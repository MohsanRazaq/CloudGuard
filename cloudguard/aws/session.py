# import boto3
# uncomment when  you want to interact with real aws .for testing you can use this local stack wrapper
from aws_wrapper import get_boto3_session
session=get_boto3_session()
def create_session(region="us-east-1"):
    return session
    