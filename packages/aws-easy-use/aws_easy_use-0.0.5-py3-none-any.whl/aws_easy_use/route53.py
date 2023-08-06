from typing import List

import boto3


def get_record_names_by_alias_target_dns_names(alias_target_dns_names: List[str]) -> List[str]:
    """
    Get record names by alias target DNS names

    :param List[str] alias_target_dns_names: alias target DNS names
    :return: record names
    :rtype: List[str]
    """

    search_strs = [f"{x}." for x in alias_target_dns_names]

    client = boto3.client('route53')
    response = client.list_hosted_zones()
    results = []
    for hosted_zone_id in (x["Id"] for x in response["HostedZones"]):
        response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        for record_set in (x for x in response["ResourceRecordSets"] if x["Type"] == "A"):
            if record_set["AliasTarget"]["DNSName"] in search_strs:
                results.append(record_set["Name"][:-1])
    return results
