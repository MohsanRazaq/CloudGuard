from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.s3_checks import (
    check_bucket_versioning
)
from cloudguard.constants import SEPARATOR
from cloudguard.security_checks.encryption_check import check_bucket_encryption
from cloudguard.security_checks.public_access_check import check_bucket_acl

################################################################################
S3_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_bucket_acl
]


def feeder(message) -> None:
    text = str(message)
    print(text)
    write_log(text)
    
def setup_logger()->None:
    config = load_config()
    running_tasks = []
    skipped_tasks = []


    for scan_type, enabled in config.items():
        if enabled:
            running_tasks.append(scan_type)
        else:
            skipped_tasks.append(scan_type)
    message = (
    "\n"
    +" " * 25 
    +"CLOUD GUARD\n"
    + SEPARATOR
    + "\n"
    + f"Running Tasks : {', '.join(running_tasks)}\n"
    + f"Skipped Tasks : {', '.join(skipped_tasks)}\n"
    + SEPARATOR
)   
    feeder(message)

def scan_s3_buckets() -> None:
    feeder("\n" + SEPARATOR)
    feeder(" S3 SECURITY ASSESSMENT")
    feeder(SEPARATOR)
    
    for bucket in list_buckets():
        # 1. Print the header for the resource being evaluated
        feeder(f"\n[RESOURCE] {bucket}")
        
        has_issues = False

        for check in S3_CHECKS:
            result = check(bucket)

            if result:
                # 2. If an issue is found, print the formatted finding with an indent
                feeder(result)
                has_issues = True
            else:
                # 3. If result is None, explicitly report that the specific check passed!
                # We extract the check name by converting the function name cleanly
                check_name = check.__name__.replace('check_bucket_', '').title()
                feeder(f"  ↳ [PASS] {check_name}: Secure and compliant")
        
        # 4. Print a clean status summary line for this specific bucket
        if not has_issues:
            feeder(f"   Status: All checks passed for {bucket}")
            
    feeder("\n" + SEPARATOR)
    feeder(" SCAN COMPLETE")
    feeder(SEPARATOR)

        

        

def main():
    setup_logger()
    scan_s3_buckets()


if __name__ == "__main__":
    main()