from botocore.exceptions import ClientError
from cloudguard.findings import Finding


def check_user_mfa(iam_client):
    """
    Check whether IAM users have MFA enabled.
    Returns a list of Finding objects.
    """

    findings = []

    try:
        users = iam_client.list_users()["Users"]

    except ClientError as e:
        return [
            Finding(
                check="IAM User MFA",
                resource="IAM",
                passed=False,
                severity="HIGH",
                issue=f"AWS API Error: {e.response['Error']['Message']}",
                recommendation="Grant 'iam:ListUsers' permission to the CloudGuard IAM user."
            )
        ]

    for user in users:
        username = user["UserName"]

        try:
            mfa_devices = iam_client.list_mfa_devices(
                UserName=username
            )["MFADevices"]

            if mfa_devices:
                findings.append(
                    Finding(
                        check="IAM User MFA",
                        resource=username,
                        passed=True,
                        severity="LOW",
                        issue="",
                        recommendation=""
                    )
                )
            else:
                findings.append(
                    Finding(
                        check="IAM User MFA",
                        resource=username,
                        passed=False,
                        severity="HIGH",
                        issue=f"MFA is not enabled for IAM user '{username}'.",
                        recommendation="Enable MFA for this IAM user."
                    )
                )

        except ClientError as e:
            findings.append(
                Finding(
                    check="IAM User MFA",
                    resource=username,
                    passed=False,
                    severity="HIGH",
                    issue=f"Could not check MFA status: {e.response['Error']['Message']}",
                    recommendation="Grant 'iam:ListMFADevices' permission."
                )
            )

    return findings