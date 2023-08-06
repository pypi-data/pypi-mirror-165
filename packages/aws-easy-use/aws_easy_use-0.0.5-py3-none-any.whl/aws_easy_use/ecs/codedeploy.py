from typing import List
import boto3, time, enum

from . import service as ep_service
from . import task_definition as ep_task_definition
from .. import route53 as ep_route53


@enum.unique
class DEPLOYMENT_STATE(enum.Enum):
    STEADY = 1
    INSTALLING = 2
    WAITING_SWITCH_ROUTE = 3
    WAITING_TERMINATING_ORIGINAL_SET = 4


APPLICATION_NAME = lambda cluster, service: f"AppECS-{cluster}-{service}"
DEPLOYGROUP_NAME = lambda cluster, service: f"DgpECS-{cluster}-{service}"


def make_service_appspec_dict(ecs_cluster: str, ecs_service: str, task_definition_with_rev: str, appspec_ver: str):
    """
    make service appspec for codedeploy

    :param str ecs_cluster: cluster name
    :param str ecs_service: service name
    :param str task_definition_with_rev: task definition with revision ex: td:12
    :param str appspec_ver: appspec version
    :return: appspec dict
    :rtype: dict
    """

    service = ep_service.get_detail(ecs_cluster, ecs_service)

    return {
        "version": appspec_ver,
        "Resources": [
            {
                "TargetService": {
                    "Type": "AWS::ECS::Service",
                    "Properties": {
                        "TaskDefinition": ep_task_definition.get_arn(task_definition_with_rev),
                        "LoadBalancerInfo": {
                            # In a ECS service, there is only one ALB allowed.
                            "ContainerName": service["loadBalancers"][0]["containerName"],
                            "ContainerPort": service["loadBalancers"][0]["containerPort"]
                        }
                    }
                }
            }
        ]
    }


def terminate_last_deployment_original_set(ecs_cluster: str, ecs_service: str, wait_interval=5, wait_times=120) -> None:
    """
    Terminate last deployment original set

    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :param int wait_interval: wait retry interval
    :param int wait_times: wait times
    """
    if last_deployment_id := get_last_deployment_id(ecs_cluster, ecs_service):
        status = get_deployment_status(last_deployment_id, ecs_cluster, ecs_service)
        assert status == DEPLOYMENT_STATE.WAITING_TERMINATING_ORIGINAL_SET

        codedeploy_client = boto3.client('codedeploy')

        response = codedeploy_client.continue_deployment(deploymentId=last_deployment_id, deploymentWaitType='TERMINATION_WAIT')
        # TODO Check response

        waiter = codedeploy_client.get_waiter('deployment_successful')
        waiter.wait(deploymentId=last_deployment_id, WaiterConfig={'Delay': wait_interval, 'MaxAttempts': wait_times})
        time.sleep(10)

        status = get_deployment_status(last_deployment_id, ecs_cluster, ecs_service)
        assert status == DEPLOYMENT_STATE.STEADY, f"After terminating last deployment original set, the deployment is not in steady state. Got `{status}`"
    else:
        raise Exception(f"There is no last deployment for ECS cluster `{ecs_cluster}` and ECS service`{ecs_service}`")


def create_deployment(ecs_cluster: str, ecs_service: str, appspec_json_bucket: str, appspec_json_s3_path: str) -> str:
    """
    Create deployment

    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :param str appspec_json_bucket: S3 bucket that stores the appspec.json
    :param str appspec_json_s3_path: S3 path that stores the appspec.json
    :return: deployment ID
    :rtype: str
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.create_deployment(
        applicationName=APPLICATION_NAME(ecs_cluster, ecs_service),
        deploymentGroupName=DEPLOYGROUP_NAME(ecs_cluster, ecs_service),
        autoRollbackConfiguration={'enabled': False},
        revision={
            'revisionType': 'S3',
            's3Location': {
                'bucket': appspec_json_bucket,
                'key': appspec_json_s3_path,
                'bundleType': 'JSON'
            }
        }
    )
    return response["deploymentId"]


def switch_route(deployment_id: str, ecs_cluster: str, ecs_service: str, wait_interval=5, wait_times=120) -> None:
    """
    Switch route

    :param str deployment_id: deployment ID
    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :param int wait_interval: wait retry interval
    :param int wait_times: wait times
    """

    status = get_deployment_status(deployment_id, ecs_cluster, ecs_service)
    assert status == DEPLOYMENT_STATE.WAITING_SWITCH_ROUTE, f":x: Deployment `{deployment_id}` is not ready for switching route. Got `{status}`"
    
    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.continue_deployment(deploymentId=deployment_id, deploymentWaitType='READY_WAIT')
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200, ":x: Deployment `{}` switch route failed. Response status `{}`".format(deployment_id, response['ResponseMetadata']['HTTPStatusCode'])


    def wait_until_termination_inprogress():
        time.sleep(wait_interval)
        for _ in range(0, wait_times):
            if is_deployment_in_terminating_orignal_set_state(deployment_id, ecs_cluster, ecs_service):
                return True
            time.sleep(wait_interval)
        return False


    assert wait_until_termination_inprogress()


def rollback_deployment(deployment_id: str, ecs_cluster: str, ecs_service: str, wait_interval=5, wait_times=120) -> None:
    """
    Rollback deployment

    :param str deployment_id: deployment ID
    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :param int wait_interval: wait retry interval
    :param int wait_times: wait times
    """

    status = get_deployment_status(deployment_id, ecs_cluster, ecs_service)
    assert status == DEPLOYMENT_STATE.WAITING_TERMINATING_ORIGINAL_SET, f":x: Deployment `{deployment_id}` is not in WAITING_TERMINATING_ORIGINAL_SET state. Got `{status}`"
    
    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.stop_deployment(deploymentId=deployment_id, autoRollbackEnabled=True)

    time.sleep(wait_interval)

    for _ in range(0, wait_times):
        # It will create a new rollback deployment
        if rollback_deployment_id := get_last_deployment_id(ecs_cluster, ecs_service):
            response = codedeploy_client.get_deployment(deploymentId=rollback_deployment_id)
            if response["deploymentInfo"]["status"] == "Succeeded":
                break
            time.sleep(wait_interval)
        else:
            raise Exception(f"There should be last deployment which is rollback deployment itself for ECS cluster `{ecs_cluster}` and ECS service `{ecs_service}` for rollback source deployment ID `{deployment_id}`")


def get_auto_switch_route_time_str(ecs_cluster: str, ecs_service: str) -> str:
    """
    Get auto switch route time is string format

    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :return: auto switch route time
    :rtype: str
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.get_deployment_group(
        applicationName=APPLICATION_NAME(ecs_cluster, ecs_service),
        deploymentGroupName=DEPLOYGROUP_NAME(ecs_cluster, ecs_service)
    )
    wait_time = response["deploymentGroupInfo"]["blueGreenDeploymentConfiguration"]["deploymentReadyOption"]
    auto_switch_route_time_total_mins = wait_time.get("waitTimeInMinutes", 0)
    auto_switch_route_time_total_hours = int(auto_switch_route_time_total_mins) / 60
    return "{:.0f} days {:.0f} hours {:.0f} mins".format(auto_switch_route_time_total_hours / 24, auto_switch_route_time_total_hours % 24, int(auto_switch_route_time_total_mins) % 60)


def wait_until_ready(deployment_id: str, wait_times: int, wait_interval: int):
    """
    wait and determine if the new deployment status is ready to switch route

    :param str deployment_id: codedeploy deployment id
    :param int wait_times: waiting max times
    :param int wait_interval: waiting interval
    :return: latest deployment is now ready
    :rtype: boolean
    """

    codedeploy_client = boto3.client('codedeploy')

    for _ in range(0, wait_times):
        time.sleep(wait_interval)
        response = codedeploy_client.get_deployment(deploymentId=deployment_id)
        if response['deploymentInfo']['status'] == 'Ready':
            return
        
    if "errorInformation" in response['deploymentInfo']:
        return response['deploymentInfo']["errorInformation"]["message"]
    else:
        return f"Deployment status in `{response['deploymentInfo']['status']}` without reason"


def wait_until_installation_steady(deployment_id: str, ecs_cluster: str, ecs_service: str, wait_times: int, wait_interval: int):
    """
    wait and determine if the new deployment is in steady state

    :param str deployment_id: codedeploy deployment id
    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :param int wait_times: waiting max times
    :param int wait_interval: waiting interval
    :return: is_finally_in_steady_state
    :rtype: bool
    """

    for _ in range(0, wait_times): # wait at most 10 mins(30sec * 20)
        service = ep_service.get_detail(ecs_cluster, ecs_service)
        results = [x for x in service["taskSets"] if "externalId" in x and x["externalId"] == deployment_id]
        if len(results) != 1:
            raise Exception(f"There should be only 1 deployment task set for `{ecs_cluster}` cluster `{ecs_service}` service ... but got '{results}'")
        task_set = results[0]
        if task_set["stabilityStatus"] == "STEADY_STATE":
            return
        time.sleep(wait_interval)

    events_str =      "\n".join([f"{event['id']}, {event['createdAt']}, {event['message']}" for event in service["events"][:5]])
    deployments_str = "\n".join([f"{deployment['id']}, {deployment['status']}, {deployment['rolloutStateReason']}, {deployment['rolloutState']}" for deployment in service["deployments"]])

    if deployments_str:
        return f"Deployments Status\n{deployments_str}\nRecent 5 events\n{events_str}"
    else:
        return f"Recent 5 events\n{events_str}"


def get_last_deployment_id(ecs_cluster: str, ecs_service: str):
    """
    get last deployment id

    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :return: last deployment id
    :rtype: str
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.get_deployment_group(
        applicationName=APPLICATION_NAME(ecs_cluster, ecs_service),
        deploymentGroupName=DEPLOYGROUP_NAME(ecs_cluster, ecs_service)
    )
    if "lastAttemptedDeployment" in response['deploymentGroupInfo']:
        return response['deploymentGroupInfo']['lastAttemptedDeployment']['deploymentId']
    else:
        return None


def get_deployment_status(deployment_id: str, ecs_cluster: str, ecs_service: str):
    """
    get deployment status

    :param str deployment_id: deployment id
    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :return: deployment status
    :rtype: DEPLOYMENT_STATE
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.get_deployment(deploymentId=deployment_id)
    status = response['deploymentInfo']['status']
    
    if status == 'Succeeded' or status == 'Failed' or status == 'Stopped':
        return DEPLOYMENT_STATE.STEADY

    elif status == 'Created' or status == 'Queued' or status == 'Baking':
        return DEPLOYMENT_STATE.INSTALLING

    elif status == 'Ready':
        return DEPLOYMENT_STATE.WAITING_SWITCH_ROUTE

    elif status == 'InProgress':
        if is_deployment_in_terminating_orignal_set_state(deployment_id, ecs_cluster, ecs_service):
            return DEPLOYMENT_STATE.WAITING_TERMINATING_ORIGINAL_SET
        else:
            return DEPLOYMENT_STATE.INSTALLING

    else:
        raise Exception("Exception for un-handling deployment status '{}'".format(status))


def is_deployment_in_terminating_orignal_set_state(deployment_id: str, ecs_cluster: str, ecs_service: str):
    """
    terminating original set state means all deployment lifecycle events succeeded

    :param str deployment_id: deployment id
    :param str ecs_cluser: cluster name
    :param str ecs_service: service name
    :return all deployment lifecycle events succeeded
    :rtype booleen
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.get_deployment_target(
        deploymentId= deployment_id,
        targetId='{}:{}'.format(ecs_cluster,ecs_service)
    )

    events = response["deploymentTarget"]["ecsTarget"]["lifecycleEvents"]
    not_succeeded_events = [event for event in events if event["status"] != 'Succeeded']
    for not_succeeded_event in not_succeeded_events:
        print('Deployment is still in stage {}'.format(not_succeeded_event["lifecycleEventName"]))
    return bool(not_succeeded_events == [])


def cancel_deployment(deployment_id: str):
    """
    :param str deployment_id: deployment id
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.stop_deployment(deploymentId=deployment_id, autoRollbackEnabled=False)
    # TODO Check response
    while True:
        response = codedeploy_client.get_deployment(deploymentId=deployment_id)
        status = response['deploymentInfo']['status']
        if  status == 'Stopped':
            return
        time.sleep(2)


def get_blue_set_test_domains(ecs_cluster: str, ecs_service: str) -> List[str]:
    """
    Get blue set load balancer test domains include host and port

    :param str ecs_cluster: ECS cluster
    :param str ecs_service: ECS service
    :return: test domains include host and port
    :rtype: List[str]
    """

    codedeploy_client = boto3.client('codedeploy')

    response = codedeploy_client.get_deployment_group(
        applicationName=APPLICATION_NAME(ecs_cluster, ecs_service),
        deploymentGroupName=DEPLOYGROUP_NAME(ecs_cluster, ecs_service)
    )

    blue_green_pairs = response["deploymentGroupInfo"]["loadBalancerInfo"]["targetGroupPairInfoList"]
    if len(blue_green_pairs) != 1:
        raise Exception(f"There should be only 1 blue green pair. Got\n{blue_green_pairs}")
    blue_green_pair = blue_green_pairs[0]

    if len(blue_green_pair["testTrafficRoute"]["listenerArns"]) != 1:
        raise Exception(f"There should be only 1 blue listener ARN. Got\n{blue_green_pair['testTrafficRoute']['listenerArns']}")
    blue_listener_arn = blue_green_pair["testTrafficRoute"]["listenerArns"][0]

    client = boto3.client('elbv2')
    response = client.describe_listeners(ListenerArns=[blue_listener_arn])

    if len(response["Listeners"]) != 1:
        raise Exception(f"There should be only 1 listener detail for ARN '{blue_listener_arn}'. Got\n{response['Listeners']}")
    test_port = response["Listeners"][0]["Port"]

    lb_dns_names = ep_service.get_all_lb_dns_names(ecs_cluster, ecs_service)
    test_domains = ep_route53.get_record_names_by_alias_target_dns_names(lb_dns_names)
    if test_domains:
        return [f"https://{test_domain}:{test_port}" for test_domain in test_domains]
    else:
        return [f"http://{test_domain}:{test_port}" for test_domain in lb_dns_names]
