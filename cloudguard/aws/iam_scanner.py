from cloudguard.security_checks.iam.check_user_mfa import check_user_mfa 
from cloudguard.security_checks.iam.check_access_last_used import check_access_last_used
from cloudguard.utils.logger import feeder
IAM_SECURITY_CHECKS = [
    check_user_mfa,
    check_access_last_used
]


def scan_iam(session):
    iam_client = session.client("iam")
    findings = []

    feeder("\n========================================")
    feeder("IAM SECURITY ASSESSMENT")
    feeder("========================================")

    for check in IAM_SECURITY_CHECKS:
        results = check(iam_client)

        for result in results:
            feeder(result)

        findings.extend(results)

    return findings,{}


