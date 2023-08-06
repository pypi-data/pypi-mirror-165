import boto3, re

from . import task_definition as ep_task_definition


def get_detail(scheduled_task_name: str):
    """
    get scheduled task

    :param str scheduled_task_name: scheduled task name
    :return: scheduled_task
    :rtype: dict
    """

    client = boto3.client('events') 
    return client.describe_rule(Name=scheduled_task_name)


def get_targets(scheduled_task_name: str):
    """
    get scheduled task targets

    :param str scheduled_task_name: scheduled task name
    :return: scheduled_task_targets
    :rtype: list
    """

    client = boto3.client('events')
    return client.list_targets_by_rule(Rule=scheduled_task_name)["Targets"]


def get_cron(scheduled_task_name: str) -> str:
    """
    get scheduled task cron

    :param str scheduled_task_name: scheduled task name
    :return: cron
    :rtype: str
    """

    response = get_detail(scheduled_task_name)

    cron_reg = r"^cron\((.+)\)$"
    if m := re.match(cron_reg, response["ScheduleExpression"]):
        return m.group(1)
    raise Exception("Scheduled task `{}` cron not match `{}` got `{}`".format(scheduled_task_name, cron_reg, response["ScheduleExpression"]))


def get_enable(scheduled_task_name: str) -> bool:
    """
    get scheduled task enable

    :param str scheduled_task_name: scheduled task name
    :return: enable
    :rtype: bool
    """

    response = get_detail(scheduled_task_name)

    return True if response["State"] == "ENABLED" else False


def get_target_task_definition_rev(scheduled_task_name: str, scheduled_task_target_name: str) -> str:
    """
    get scheduled task target task definition with revision

    :param str scheduled_task_name: scheduled task name
    :param str scheduled_task_target_name: scheduled task target name
    :return: scheduled task target task definition with revision
    :rtype: str
    """

    response = get_targets(scheduled_task_name)

    results = [target["EcsParameters"]['TaskDefinitionArn'].split('/')[1] for target in response if target['Id'] == scheduled_task_target_name]
    assert len(results) == 1, f"Multiple results for schedule task `{scheduled_task_name}` and target `{scheduled_task_target_name}`"
    return results[0]


def update(scheduled_task_name: str, cron_exp=None, enable=None):
    """
    update scheduled task

    :param str scheduled_task_name: scheduled task name
    :param str cron_exp: EX: '0 11 * * ? *'
    :param str enable: enable scheduled task?
    :return: response
    :rtype: dict
    """
    # Fixed interval "rate(1 hour)" not support

    args = {}
    if enable is not None:
        args["State"] = "ENABLED" if enable else "DISABLED"

    original_scheduled_task = get_detail(scheduled_task_name)

    client = boto3.client('events') 
    return client.put_rule(
        Name=scheduled_task_name,
        ScheduleExpression="cron({})".format(cron_exp) if cron_exp else original_scheduled_task["ScheduleExpression"],
        **args
    )


def update_target(scheduled_task_name: str, update_target_id: str, update_task_definition_with_rev: str):
    """
    update a scheduled task target
    沒列在 scheduled_task_target_task_definition 內的 target 但是 scheduled task 既有的 target 會保留
    要刪除請實作 remove_targets()

    :param str scheduled_task_name: scheduled task name
    :param str request_update_target_id: update target id
    :param str update_task_definition_with_rev: update target task definition with revision
    :return: response
    :rtype: dict
    """

    scheduled_targets = get_targets(scheduled_task_name)
    assert update_target_id in [x["Id"] for x in scheduled_targets]
    for target in scheduled_targets:
        if target["Id"] == update_target_id:
            assert "EcsParameters" in target, "Update target '{}' but target without 'EcsParameters'".format(target["Id"])
            target["EcsParameters"]["TaskDefinitionArn"] = ep_task_definition.get_arn(update_task_definition_with_rev)
 
    client = boto3.client('events') 
    return client.put_targets(Rule=scheduled_task_name, Targets=scheduled_targets)
