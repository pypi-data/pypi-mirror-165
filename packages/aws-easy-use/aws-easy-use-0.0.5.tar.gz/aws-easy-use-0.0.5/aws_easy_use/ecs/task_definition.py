import json, boto3


def get_arn(task_definition_with_rev: str):
    """
    get task definition ARN

    :param str task_definition_with_rev: task definition with revision
    :return: task definition ARN
    :rtype: str
    """

    client = boto3.client('ecs') 
    return client.describe_task_definition(taskDefinition=task_definition_with_rev)["taskDefinition"]["taskDefinitionArn"]


def get_request_template_dict(task_definition_with_rev: str) -> dict:
    """
    Create request template dict for 'client.register_task_definition(**task_definition_request_dict)'

    :param str task_definition_with_rev: task definition family with revision (default is latest). EX: ted-fargate:22
    :return: get task definition request  template dict
    :rtype: dict
    """

    client = boto3.client('ecs')
    response = client.describe_task_definition(taskDefinition=task_definition_with_rev)

    # {
    #     'taskDefinition': {
    #         'taskDefinitionArn': 'string',
    #         'containerDefinitions': [
    #             ...
    #             'name': 'string',
    #             'image': 'string',
    #             'command': [
    #                 'string',
    #             ],
    #             'environment': [
    #                 {
    #                     'name': 'string',
    #                     'value': 'string'
    #                 },
    #             ],
    #             'secrets': [
    #                 {
    #                     'name': 'string',
    #                     'valueFrom': 'string'
    #                 },
    #             ],

    # Remove not use arguments
    response["taskDefinition"].pop("registeredAt", None)
    response["taskDefinition"].pop("deregisteredAt", None)
    response["taskDefinition"].pop("taskDefinitionArn", None)
    response["taskDefinition"].pop("revision", None)
    response["taskDefinition"].pop("status", None)
    response["taskDefinition"].pop("requiresAttributes", None)
    response["taskDefinition"].pop("compatibilities", None)
    response["taskDefinition"].pop("registeredAt", None)
    response["taskDefinition"].pop("deregisteredAt", None)
    response["taskDefinition"].pop("registeredBy", None)

    return response["taskDefinition"]


def register_task_definition_from_json_file(json_file: str):
    """
    register new revision for a task definition by json file from function 'make_task_definition_from_json_file'

    :param str json_file: json file from function 'make_task_definition_from_json_file'
    :return: the new revision
    :rtype: str, int
    """

    with open(json_file, "r") as fin:
        client = boto3.client('ecs')
        response = client.register_task_definition(**json.load(fin))
        print("New task definition '{}:{}'".format(response["taskDefinition"]["family"], response["taskDefinition"]["revision"]))
        return response["taskDefinition"]["family"], response["taskDefinition"]["revision"]
