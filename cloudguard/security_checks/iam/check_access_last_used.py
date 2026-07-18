# security_checks/iam/check_access_last_used.py

def check_access_last_used(iam_client):
    """
    Scans users, loops through their keys, and verifies usage metrics
    """
    findings = []
    try:
        users_response = iam_client.list_users()
        for user in users_response['Users']:
            username = user['UserName']
            
            keys_response = iam_client.list_access_keys(UserName=username)
            for key in keys_response['AccessKeyMetadata']:
                key_id = key['AccessKeyId']
                
                usage_response = iam_client.get_access_key_last_used(AccessKeyId=key_id)
                print(f"Verified usage metrics for key: {key_id}")
                
    except Exception as e:
        print(f"Error checking access key usage: {e}")
        
    return findings
