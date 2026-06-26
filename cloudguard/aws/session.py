import boto3


def create_session(region="us-east-1"):
    return boto3.client(
        "s3",
        region_name=region
    )
    