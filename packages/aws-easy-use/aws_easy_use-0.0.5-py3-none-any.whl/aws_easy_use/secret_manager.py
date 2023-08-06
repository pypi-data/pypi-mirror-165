import boto3, re


def is_resource(the_arn: str):
    """
    is the ARN is a secret manager resource?

    :param str the_arn: the ARN
    :return: is the ARN is a secret manager resource?
    :rtype: bool
    """

    # arn:aws:secretsmanager:ap-northeast-1:038528481894:secret:ep/ECS-secret/test-XlIeIr
    return the_arn.startswith("arn:aws:secretsmanager:")


def is_reference_key_existed(reference_key_arn: str, region: str = None):
    """
    is reference secret key existed?

    :param str reference_key_arn: reference ARN with key
    :return: is reference key existed?
    :rtype: bool
    """
    # arn:aws:secretsmanager:ap-northeast-1:{account_id}:secret:blabo-dev-aurora-mysql-admin20220819015905167800000001-aaiAzJ:password::

    arn_format = r'^(arn:aws:secretsmanager:.+:\d+:secret:.+):(.+)::$'

    if m := re.match(arn_format, reference_key_arn):
        secret_arn, secret_key = m.groups()

        client = boto3.client('secretsmanager', region_name=region)
        return secret_arn in [secret["ARN"] for secret in client.list_secrets()["SecretList"]]

        result = client.get_secret_value(secret_arn) # May be SecretBinary which we cannot verify

    else:
        raise Exception(f"Invalid 'reference_key_arn' need format\n{arn_format}\nGot\n{reference_key_arn}")
