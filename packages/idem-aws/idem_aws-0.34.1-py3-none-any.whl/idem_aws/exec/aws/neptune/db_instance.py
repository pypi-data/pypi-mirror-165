from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.neptune.db_instance"


async def get(
    hub, ctx, name: str, resource_id: str = None, filters: List = None
) -> Dict:
    """
    Fetch and use an un-managed neptune db instance as a data-source.

    Args:
        name(string): The name of the Idem state
        resource_id(string, optional): AWS Neptune DBInstanceIdentifier to identify the resource.
        filters(list, optional): A filter that specifies one or more DB instances to describe.
            Supported filters:
            db-cluster-id - Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list will only include information about the DB instances associated with the DB clusters identified by these ARNs.
            engine - Accepts an engine name (such as neptune ), and restricts the results list to DB instances created by that engine.
        Note that if filters used matches more than one neptune db instance, idem will default to fetching the first result.
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.neptune.db_instance.search_raw(
        ctx=ctx, name=name, resource_id=resource_id, filters=filters
    )
    if not ret["result"]:
        if "DBInstanceNotFoundFault" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=RESOURCE_TYPE, name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBInstances"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result

    resource = ret["ret"]["DBInstances"][0]
    if len(ret["ret"]["DBInstances"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=RESOURCE_TYPE,
                resource_id=resource.get("DBInstanceIdentifier"),
            )
        )
    arn = resource["DBInstanceArn"]
    # get tags
    tags = await hub.exec.aws.neptune.tag.get_tags_for_resource(ctx, resource_arn=arn)
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    tags = tags["ret"]
    result[
        "ret"
    ] = await hub.tool.aws.neptune.conversion_utils.convert_raw_db_instance_to_present(
        raw_resource=resource, idem_resource_name=name, tags=tags
    )
    return result


async def list_(hub, ctx, name, filters: List = None) -> Dict:
    """
    Use a list of un-managed neptune db instances as a data-source. Supply one of the inputs as the filter.

    Args:
        name(string): The name of idem state.
        filters(list, optional): A filter that specifies one or more DB instances to describe.
            Supported filters:
            db-cluster-id - Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list will only include information about the DB instances associated with the DB clusters identified by these ARNs.
            engine - Accepts an engine name (such as neptune ), and restricts the results list to DB instances created by that engine.
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.neptune.db_instance.search_raw(
        ctx=ctx, name=name, filters=filters
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBInstances"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result
    for db_instance in ret["ret"]["DBInstances"]:
        db_instance_identifier = db_instance.get("DBInstanceIdentifier")
        arn = db_instance["DBInstanceArn"]
        tags = await hub.exec.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=arn
        )
        tags = tags["ret"]
        result["ret"].append(
            await hub.tool.aws.neptune.conversion_utils.convert_raw_db_instance_to_present(
                raw_resource=db_instance,
                idem_resource_name=db_instance_identifier,
                tags=tags,
            )
        )
    return result
