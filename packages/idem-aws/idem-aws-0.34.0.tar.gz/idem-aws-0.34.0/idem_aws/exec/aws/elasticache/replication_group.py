from typing import Dict


async def get(
    hub,
    ctx,
    name,
    resource_id: str,
) -> Dict:
    """
    Use an un-managed Elasticache replication group as a data-source.
    if both resource_id and name are not None, search is done with resource_id else by name

    Args:
        name(Text): The name of the Idem state. It is used as ReplicationGroupID during resource creation
        resource_id(Text): The replication group identifier.

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.elasticache.describe_replication_groups(
        ctx=ctx,
        ReplicationGroupId=resource_id,
    )
    if not ret["result"]:
        if "ReplicationGroupNotFoundFault" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.elasticache.replication_group", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] = list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["ReplicationGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.elasticache.replication_group", name=name
            )
        )
        return result
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    resource = ret["ret"]["ReplicationGroups"][0]
    before_tag = await hub.exec.boto3.client.elasticache.list_tags_for_resource(
        ctx, ResourceName=resource.get("ARN")
    )
    if not before_tag["result"]:
        result["result"] = False
        result["comment"] += list(before_tag["comment"])
        return result
    resource["Tags"] = before_tag["ret"].get("TagList", [])
    result[
        "ret"
    ] = hub.tool.aws.elasticache.conversion_utils.convert_raw_elasticache_replication_group_to_present(
        ctx, raw_resource=resource, idem_resource_name=name
    )
    return result
