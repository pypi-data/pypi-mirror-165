from typing import Dict


async def get(hub, ctx, name: str) -> Dict:
    """

    Retrieves the password policy for the Amazon Web Services account.

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.iam.get_account_password_policy(ctx)

    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.password_policy", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.iam.conversion_utils.convert_raw_password_policy_to_present(
        ctx, raw_password_policy=ret["ret"]["PasswordPolicy"]
    )
    return result
