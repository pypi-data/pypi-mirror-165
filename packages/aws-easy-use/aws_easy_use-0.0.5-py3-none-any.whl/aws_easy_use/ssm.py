import boto3


def is_resource(the_arn: str):
    """
    is the ARN is a SSM resource?

    :param str the_arn: the ARN
    :return: is the ARN is a SSM resource?
    :rtype: bool
    """

    # arn:aws:ssm:ap-northeast-1:038528481894:parameter/ep-test-ssh
    return the_arn.startswith("arn:aws:ssm:")


def is_reference_existed(reference_arn: str):
    """
    is reference existed?

    :param str reference_arn: reference ARN
    :return: is reference existed?
    :rtype: bool
    """

    client = boto3.client('ssm')
    # "arn:aws:ssm:ap-northeast-1:038528481894:parameter/ep-test-ssh"
    parameters = client.get_parameters(Names=[reference_arn.split(':parameter/')[1]])["Parameters"]
    return reference_arn in [parameter["ARN"] for parameter in parameters]
