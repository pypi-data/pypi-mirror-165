from typing import List

import boto3, enum, time


@enum.unique
class DEPLOY_TYPE(enum.Enum):
    CODEDEPLOY = 1
    ROLLING_UPDATE = 2


def get_detail(cluster_name: str, service_name: str) -> dict:
    """
    get service detail

    :param str cluster_name: ECS cluster
    :param str service_name: ECS service
    :return: service
    :rtype: dict
    """

    client = boto3.client('ecs')
    response = client.describe_services(cluster=cluster_name, services=[service_name])
    assert len(response["services"]) == 1, "There should be only one service '{}' in Cluster '{}'. Got '{}'".format(service_name, cluster_name, response["services"])
    return response["services"][0]


def get_all_lb_dns_names(cluster_name: str, service_name: str) -> List[str]:
    """
    get service all load balancer DNS names

    :param str cluster_name: ECS cluster
    :param str service_name: ECS service
    :return: load balancer DNS names
    :rtype: List[str]
    """

    service = get_detail(cluster_name, service_name)
    target_group_arns = [
        lb["targetGroupArn"]
        for task_set in service["taskSets"]
        for lb in task_set["loadBalancers"]
    ]

    client = boto3.client('elbv2')
    response = client.describe_target_groups(TargetGroupArns=target_group_arns)

    if len(response["TargetGroups"]) != len(target_group_arns):
        return Exception(f"Unable to get exaclt {len(target_group_arns)} target group for ARNs `{target_group_arns}`")

    response = client.describe_load_balancers(
        LoadBalancerArns=[
            lb_arn
            for target_group in response["TargetGroups"]
            for lb_arn in target_group["LoadBalancerArns"]
        ]
    )
    return [x["DNSName"] for x in response["LoadBalancers"]]


def get_task_definition_with_rev(cluster_name: str, service_name: str) -> str:
    """
    get service task definition with revision

    :param str cluster_name: ECS cluster
    :param str service_name: ECS service
    :return: task_definition_with_rev
    :rtype: str
    """

    service = get_detail(cluster_name, service_name)
    return service["taskDefinition"].split('/')[1]


def get_deploy_type(cluster_name: str, service_name: str) -> DEPLOY_TYPE:
    """
    get service task definition with revision

    :param str cluster_name: ECS cluster
    :param str service_name: ECS service
    :return: deploy_type
    :rtype: DEPLOY_TYPE
    """

    service = get_detail(cluster_name, service_name)
    if "deploymentController" in service:
        assert service["deploymentController"]["type"] == "CODE_DEPLOY", "Unsupport deployment type for '{}' cluster '{}' service for type '{}'".format(cluster_name, service_name, service["deploymentController"]["type"])
        return DEPLOY_TYPE.CODEDEPLOY
    else:
        return DEPLOY_TYPE.ROLLING_UPDATE


def update_service(cluster_name: str, service_name: str, task_definition_with_rev=None, auto_rollback=False, wait_interval=5, wait_times=120, re_deploy=False) -> None:
    """
    get service task definition with revision

    :param str cluster_name: ECS cluster
    :param str service_name: ECS service
    :param str task_definition_with_rev: task definition with revision
    :param bool auto_rollback: rollback when failed
    :param int wait_interval: wait retry interval
    :param int wait_times: wait times
    """

    if re_deploy:
        assert task_definition_with_rev is None, "Re-deploy should not give task_definition_rev"

        kw = {
            "forceNewDeployment": True
        }
    else:
        kw = {
            "taskDefinition": task_definition_with_rev
        }

    client = boto3.client('ecs')
    response = client.update_service(
        cluster=cluster_name,
        service=service_name,
        deploymentConfiguration={
            "deploymentCircuitBreaker": {
                # The deployment circuit breaker determines whether a service deployment will fail if the service can't reach a steady state. 
                # If deployment circuit breaker is enabled, a service deployment will transition to a failed state and stop launching new tasks. 
                # If rollback is enabled, when a service deployment fails, the service is rolled back to the last deployment that completed successfully.
                "enable": True,
                "rollback": auto_rollback
            }
        },
        healthCheckGracePeriodSeconds=10,
        **kw
    )
    # TODO Check response

    waiter = client.get_waiter('services_stable')
    waiter.wait(cluster=cluster_name, services=[service_name], WaiterConfig={'Delay': wait_interval, 'MaxAttempts': wait_times})
    time.sleep(20)

    service = get_detail(cluster_name, service_name)
    cur_task_definition_with_rev = service["taskDefinition"].split('/')[1]
    assert cur_task_definition_with_rev == task_definition_with_rev, f"Task definition not update to `{task_definition_with_rev}` for cluster `{cluster_name}` service `{service_name}`. Got `{cur_task_definition_with_rev}`"

    results = [x for x in service["deployments"] if x["status"] == "PRIMARY"]
    assert len(results) == 1, f"There is no Primary deployment for cluster `{cluster_name}` service `{service_name}`"
    primary_deployment = results[0]
    assert primary_deployment["rolloutState"] == "COMPLETED", f"After waiting, primary deployment still not COMPLETED for cluster `{cluster_name}` service `{service_name}`. Got primarry deployment ```{primary_deployment}```"
    primary_deployment_cur_task_definition_with_rev = primary_deployment["taskDefinition"].split('/')[1]
    assert primary_deployment_cur_task_definition_with_rev == task_definition_with_rev, "After waiting, primary deployment still not update to task definition `{}` for cluster `{}` service `{}`. Got `{}`".format(task_definition_with_rev, cluster_name, service_name, primary_deployment["taskDefinition"])
