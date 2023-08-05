"""This module defines the get and list methods for AWS neptune db cluster parameter group."""
from typing import Dict

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.neptune.db_cluster_parameter_group"


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """Fetch and use an unmanaged db_cluster_parameter_group as a data-source.

    It also fetches the db cluster parameters for the supplied resource_id.
    Filters is not supported yet as per boto3 documentation for this resource.

    Args:
        hub: The redistributed pop central hub
        ctx: idem context
        name(str): Idem name of the resource
        resource_id(str, Optional): DBClusterParameterGroupName of the resource in AWS

    Note:
        At the time of writing this module, filters parameter is not supported for this resource as per
        AWS documentation so idem-aws has omitted it.

    Returns idem object representation for db_cluster_parameter_group found if resource_id was specified.
    If resource_id wasn't specified, it returns the first resource found.
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.neptune.db_cluster_parameter_group.search_raw(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not ret["result"]:
        if "DBParameterGroupNotFoundFault" in str(ret["comment"]):
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
    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result

    resource = ret["ret"]["DBClusterParameterGroups"][0]
    resource_id = resource.get("DBClusterParameterGroupName")
    if len(ret["ret"]["DBClusterParameterGroups"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=RESOURCE_TYPE, resource_id=resource_id
            )
        )
    arn = resource["DBClusterParameterGroupArn"]
    # get parameters
    parameters_raw = await hub.exec.boto3.client.neptune.describe_db_cluster_parameters(
        ctx=ctx, DBClusterParameterGroupName=resource_id
    )
    if not parameters_raw["result"]:
        result["result"] = False
        result["comment"].append(parameters_raw["comment"])
        return result
    parameters_raw = parameters_raw.get("ret")
    parameters = parameters_raw.get("Parameters")

    # get tags
    tags = await hub.exec.aws.neptune.tag.get_tags_for_resource(ctx, resource_arn=arn)
    if not tags["result"]:
        result["result"] = False
        result["comment"].append(tags["comment"])
        return result
    tags = tags["ret"]
    result[
        "ret"
    ] = await hub.tool.aws.neptune.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
        raw_resource=resource, idem_resource_name=name, tags=tags, parameters=parameters
    )
    return result


async def list_(hub, ctx, name) -> Dict:
    """Use a list of un-managed neptune db cluster parameter groups as a data-source.

    Args:
        hub: The redistributed pop central hub
        ctx: idem context
        name(str): The name of idem state.

    Note:
        At the time of writing this module, filters parameter is not supported for this resource as per
        AWS documentation so idem-aws has omitted it.
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.neptune.db_cluster_parameter_group.search_raw(
        ctx=ctx, name=name
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result
    for db_cluster_parameter_group in ret["ret"]["DBClusterParameterGroups"]:
        db_cluster_parameter_group_name = db_cluster_parameter_group.get(
            "DBClusterParameterGroupName"
        )
        arn = db_cluster_parameter_group["DBClusterParameterGroupArn"]

        # get tags
        tags = await hub.exec.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=arn
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"].append(tags["comment"])
            return result
        tags = tags["ret"]

        # get parameters
        parameters_raw = (
            await hub.exec.boto3.client.neptune.describe_db_cluster_parameters(
                ctx=ctx, DBClusterParameterGroupName=db_cluster_parameter_group_name
            )
        )
        if not parameters_raw["result"]:
            result["result"] = False
            result["comment"].append(parameters_raw["comment"])
            return result
        parameters_raw = parameters_raw.get("ret")
        parameters = parameters_raw.get("Parameters")

        result["ret"].append(
            await hub.tool.aws.neptune.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
                raw_resource=db_cluster_parameter_group,
                idem_resource_name=db_cluster_parameter_group_name,
                tags=tags,
                parameters=parameters,
            )
        )
    return result
