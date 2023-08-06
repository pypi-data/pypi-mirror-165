import boto3


def get_image_uri(repo_name: str) -> str:
    """
    get image uri

    :param str repo_name: ecr repo name
    :return: image uri
    :rtype: str
    """

    client = boto3.client('ecr')
    response = client.describe_repositories(
        repositoryNames=[repo_name]
    )

    assert len(response["repositories"]) == 1, "There should be only one ECR repository but got '{}'".format(response)
    return response["repositories"][0]["repositoryUri"]


def get_image_registry(repo_name: str) -> str:
    """
    get image registry

    :param str repo_name: ecr repo name
    :return: image registry
    :rtype: str
    """

    client = boto3.client('ecr')
    response = client.describe_repositories(
        repositoryNames=[repo_name]
    )

    assert len(response["repositories"]) == 1, "There should be only one ECR repository but got '{}'".format(response)
    return response["repositories"][0]["repositoryUri"].split("/")[0]


def is_registry(registry: str):
    """
    is the ecr registry

    :param str registry: ECR registry
    :return: is the registry exist
    :rtype: boolean
    """

    client = boto3.client('ecr')
    response = client.describe_registry()
    return registry == "{}.dkr.ecr.{}.amazonaws.com".format(response["registryId"], client.meta.region_name)


def has_repo(repo_name: str):
    """
    does ecr image exist in ecr

    :param str repo_name: ecr repo name
    :return: repo exist in ecr
    :rtype: boolean
    """

    client = boto3.client('ecr')
    try:
        client.describe_repositories(repositoryNames=[repo_name])
        return True
    except client.exceptions.RepositoryNotFoundException:
        return False


def does_repo_has_tag(repo_name: str, tag: str):
    """
    does ecr repo exist with tag

    :param str repo_name: ecr repo name
    :return: repo with tag exist in ecr 
    :rtype: boolean
    """
    
    client = boto3.client('ecr')
    response = client.list_images(repositoryName=repo_name)
    return tag in [x["imageTag"] for x in response["imageIds"]]
