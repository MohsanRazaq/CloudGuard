import boto3
import run_mock_aws
def create_session(region="us-east-1"):
    return boto3.Session(
        region_name=region
    )
    
    
# 1. Initialize your session
session = create_session()

# 2. Generate a client (e.g., IAM)
client = session.client('iam')

# 3. Inspect the hidden meta endpoint URL
active_endpoint = client.meta.endpoint_url
print(f"\n🔍 Currently connected to: {active_endpoint}")

# 4. Print an explicit warning status
if "localhost" in active_endpoint or "127.0.0.1" in active_endpoint:
    print("⚠️  STATUS: SAFE! You are running on MOCK AWS (Moto). No real charges.")
else:
    print("🚨 STATUS: LIVE PRODUCTION! You are hitting REAL AWS servers.")
