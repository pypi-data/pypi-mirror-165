from typing import Dict


async def get(
    hub,
    ctx,
    name,
    auto_scaling_group_name: str,
    resource_id: str = None,
    policy_type: str = None,
) -> Dict:
    """
    Use an un-managed scaling policy as a data-source. Supply one of the inputs as the filter.
    Policy name is the resource_id for autoscaling policy. If both resource_id and policy_name are
    not None search is done using resource_id.

    Args:
        name(Text): The name of the Idem state.
        auto_scaling_group_name(Text): The name of the Auto Scaling group.
        resource_id(Text, optional): policy name of an autoScalingGroup's policy.
        policy_type(Text, optional): policy type of an autoScalingGroup's policy. This is used to fetch a policy if resource_id is not specified.
    """
    result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.autoscaling.describe_policies(
            ctx=ctx,
            AutoScalingGroupName=auto_scaling_group_name,
            PolicyNames=[resource_id],
        )
    else:
        ret = await hub.exec.boto3.client.autoscaling.describe_policies(
            ctx=ctx,
            AutoScalingGroupName=auto_scaling_group_name,
            PolicyTypes=[policy_type] if policy_type else None,
        )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["ScalingPolicies"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.autoscaling.scaling_policy", name=name
            )
        )
        return result

    resource = ret["ret"]["ScalingPolicies"][0]
    if len(ret["ret"]["ScalingPolicies"]) > 1:
        result["comment"].append(
            f"More than one aws.autoscaling.scaling_policy resource was found. Use resource {resource.get('PolicyName')}"
        )
    result[
        "ret"
    ] = hub.tool.aws.autoscaling.conversion_utils.convert_raw_scaling_policy_to_present(
        ctx, raw_resource=resource
    )
    return result
