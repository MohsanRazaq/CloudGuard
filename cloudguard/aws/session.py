import boto3

def create_session(region="us-east-1"):
    return boto3.Session(
        region_name=region
    )