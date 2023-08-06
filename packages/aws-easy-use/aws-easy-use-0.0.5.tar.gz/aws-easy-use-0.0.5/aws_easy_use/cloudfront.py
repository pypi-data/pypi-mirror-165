from typing import List
import boto3


def is_distribution_id_existed(distribution_id: str) -> bool:
    """
    Is distribution id existed

    :param str distribution_id: distribution id
    :return: is distribution id existed?
    :rtype: bool
    """

    client = boto3.client('cloudfront')

    marker = ""
    while response := client.list_distributions(Marker=marker, MaxItems="1"):
        if distribution_id in [x["Id"] for x in response["DistributionList"]["Items"]]:
            return True

        else:
            if response["DistributionList"]["IsTruncated"]:
                marker = response["DistributionList"]["NextMarker"]

            else:
                return False


def invalidate_distribution(distribution_id: str, paths: List[str], request_id: str, wait_interval=5, wait_times=120) -> None:
    """
    Invalidate distribution

    :param str distribution_id: distribution id
    :param list paths: paths
    """

    client = boto3.client('cloudfront')
    response = client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            "Paths": {
                "Quantity": len(paths),
                "Items":    paths
            },
            "CallerReference": request_id 
        }
    )

    client.get_waiter('invalidation_completed').wait(
        DistributionId=distribution_id,
        Id=response["Invalidation"]["Id"],
        WaiterConfig={
            'Delay':       wait_interval,
            'MaxAttempts': wait_times
        }
    )
