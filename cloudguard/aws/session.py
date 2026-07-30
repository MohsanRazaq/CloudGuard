import boto3
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()

def create_session(region="us-east-1"):
    """
    Creates a standard boto3 Session.
    boto3 automatically detects AWS_ENDPOINT_URL if set in the environment.
    """
    return boto3.Session(region_name=region)