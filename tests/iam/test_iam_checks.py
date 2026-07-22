import os
import pytest
import boto3
from moto import mock_aws

# Import your modular IAM plugins
from plugins.iam.check_user_mfa import Plugin as MfaPlugin
from plugins.iam.check_access_last_used import Plugin as AccessKeyPlugin


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Sets dummy environment variables so Boto3 never hits real AWS."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


# ==============================================================================
# IAM MFA TESTS
# ==============================================================================

@mock_aws
def test_iam_user_without_mfa_is_flagged():
    iam_client = boto3.client("iam", region_name="us-east-1")
    test_user = "vulnerable-no-mfa-user"
    iam_client.create_user(UserName=test_user)

    plugin = MfaPlugin()
    context = {"iam_client": iam_client}
    findings = plugin.execute(context)

    # Find finding belonging to our target user
    target_finding = next((f for f in findings if test_user in f.resource), None)
    assert target_finding is not None
    assert target_finding.passed is False


@mock_aws
def test_iam_user_with_mfa_passes():
    iam_client = boto3.client("iam", region_name="us-east-1")
    test_user = "secure-mfa-user"
    iam_client.create_user(UserName=test_user)
    
    iam_client.enable_mfa_device(
        UserName=test_user,
        SerialNumber=f"arn:aws:iam::123456789012:mfa/{test_user}",
        AuthenticationCode1="123456",
        AuthenticationCode2="654321"
    )

    plugin = MfaPlugin()
    context = {"iam_client": iam_client}
    findings = plugin.execute(context)

    target_finding = next((f for f in findings if test_user in f.resource), None)
    assert target_finding is not None
    assert target_finding.passed is True


# ==============================================================================
# IAM ACCESS KEY USAGE TESTS
# ==============================================================================

@mock_aws
def test_unused_access_key_is_flagged():
    iam_client = boto3.client("iam", region_name="us-east-1")
    test_user = "stale-key-user"
    iam_client.create_user(UserName=test_user)
    
    # Create an access key that has never been used
    key_response = iam_client.create_access_key(UserName=test_user)
    access_key_id = key_response["AccessKey"]["AccessKeyId"]

    plugin = AccessKeyPlugin()
    context = {"iam_client": iam_client}
    findings = plugin.execute(context)

    # Verify that the unused access key triggers a failure finding
    target_finding = next((f for f in findings if access_key_id in str(f.resource)), None)
    assert target_finding is not None
    assert target_finding.passed is False


@mock_aws
def test_iam_user_without_keys_passes():
    iam_client = boto3.client("iam", region_name="us-east-1")
    test_user = "keyless-user"
    iam_client.create_user(UserName=test_user)

    plugin = AccessKeyPlugin()
    context = {"iam_client": iam_client}
    findings = plugin.execute(context)

    # Users with zero access keys should not have active key warnings
    target_finding = next((f for f in findings if test_user in str(f.resource)), None)
    # Depending on your plugin logic, either no finding is generated or it passes cleanly
    if target_finding:
        assert target_finding.passed is True