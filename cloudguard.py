from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.findings import Finding
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.s3_checks import (
    check_bucket_versioning
)
from cloudguard.security_checks.encryption_checker import check_bucket_encryption

def setup_logger():
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
    + "=" * 60
    + "\n"
    + "CloudGuard Scan Started\n"
    + f"Running Tasks : {', '.join(running_tasks)}\n"
    + f"Skipped Tasks : {', '.join(skipped_tasks)}\n"
    + "=" * 60
)
    write_log(message)
    print(message)

def discover_resources():
    print("\n=== S3 Discovery ===")
    write_log("\n=== S3 Discovery ===")

    for bucket in list_buckets():

        discovery_message = f"[DISCOVERED] {bucket}\n"

        print(discovery_message)
        write_log(discovery_message)

        encryption_finding=check_bucket_encryption(bucket)
        if encryption_finding==None:
            msg='[PASS] Bucket Encryption Enabled'
            print(msg)
            write_log(str(msg))
        else:
            msg=encryption_finding
            print(msg)
            write_log(str(msg))

        finding = check_bucket_versioning(bucket)
        if finding:
            msg='[FAIL] Bucket Versioning Disabled'
            print(msg)
            write_log(str(msg))

def main():
    setup_logger()
    discover_resources()


if __name__ == "__main__":
    main()