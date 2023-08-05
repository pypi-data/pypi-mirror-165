import boto3.session


def __init__(hub):
    # Create a single session for everything to be run from
    hub.tool.boto3.SESSION = boto3.session.Session()


def get(hub, botocore_session=None) -> boto3.session.Session:
    """
    Get the current boto3 session.
    """
    if botocore_session is None:
        # Reset the session if need be for thread safety
        hub.tool.boto3.SESSION = boto3.session.Session()
    return hub.tool.boto3.SESSION


def kwargs(hub, ctx):
    """
    Return the kwargs for a session object from ctx.acct in a consistent way
    """
    return dict(
        region_name=hub.tool.boto3.region.get(ctx),
        api_version=ctx.acct.get("api_version"),
        use_ssl=ctx.acct.get("use_ssl", True),
        endpoint_url=ctx.acct.get("endpoint_url"),
        aws_access_key_id=ctx.acct.get("aws_access_key_id"),
        aws_secret_access_key=ctx.acct.get("aws_secret_access_key"),
        aws_session_token=ctx.acct.get("aws_session_token"),
        verify=ctx.acct.get("verify"),
    )
