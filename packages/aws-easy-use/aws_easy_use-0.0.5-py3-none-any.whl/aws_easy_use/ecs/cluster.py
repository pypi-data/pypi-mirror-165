import boto3


def get_arn(cluster_name: str):
    """
    get ARN of a cluster

    :param str cluster_name: cluster name
    :return: ARN of the cluster
    :rtype: str
    """

    client = boto3.client('ecs')
    response = client.describe_clusters(clusters=[cluster_name])
    assert len(response["clusters"]) != 0, "Cluster '{}' not found".format(cluster_name)
    assert len(response["clusters"]) == 1, "There are clusters with the same name '{}'".format(cluster_name)
    return response["clusters"][0]["clusterArn"]


def get_scheduled_task_names(cluster_name: str):
    """
    get scheduled task names in cluster

    :param str cluster_name: cluster name
    :return: scheduled_task_names
    :rtype: list
    """

    client = boto3.client('events')
    return client.list_rule_names_by_target(TargetArn=get_arn(cluster_name))["RuleNames"]
