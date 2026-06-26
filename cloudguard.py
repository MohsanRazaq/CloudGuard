from cloudguard.utils.config_loader import load_config
from cloudguard.utils.logger import write_log
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.s3_checks import (
    check_bucket_versioning
)


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

        discovery_message = f"[DISCOVERED] {bucket}"

        print(discovery_message)
        write_log(discovery_message)

        finding = check_bucket_versioning(bucket)

        if finding:
            print(finding)
            write_log(str(finding))


def main():
    setup_logger()
    discover_resources()


if __name__ == "__main__":
    main()