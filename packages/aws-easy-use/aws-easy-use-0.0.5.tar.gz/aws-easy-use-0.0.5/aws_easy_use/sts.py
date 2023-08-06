import boto3, functools


def assume_role(assume_role_arn: str, assume_role_session_name: str, assume_role_region: str, external_id: str):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kw):

            print(f"Assume role `{assume_role_arn}`")
            print(f"Before assuming role, the identity is `{get_caller_identity()}`")

            assumed_role = boto3.client('sts').assume_role(
                RoleArn =         assume_role_arn,
                RoleSessionName = assume_role_session_name,
                ExternalId=external_id
            )
            boto3.setup_default_session(
                aws_access_key_id     = assumed_role['Credentials']['AccessKeyId'],
                aws_secret_access_key = assumed_role['Credentials']['SecretAccessKey'],
                aws_session_token     = assumed_role['Credentials']['SessionToken'],
                region_name           = assume_role_region
            )

            print(f"After assuming role, the identity is `{get_caller_identity()}`")

            result = func(*args, **kw)

            boto3.setup_default_session()

            return result
        return _wrapper
    return _decorator


def get_caller_identity() -> dict:
    """
    Get caller identity

    :param str reference_arn: reference ARN
    :return: is reference existed?
    :rtype: bool
    """

    return boto3.client("sts").get_caller_identity()
