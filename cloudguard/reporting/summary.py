def print_summary(findings,bucket_count):
    severity_count = {
    "CRITICAL": 0,
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0,
}
    
    total_checks = len(findings)

    passed = 0
    failed = 0

    CRITICAL = 0
    HIGH = 0
    MEDIUM = 0
    LOW= 0
    for finding in findings:

        if finding.passed:
            passed += 1
        else:
            failed += 1

            severity = finding.severity

            if severity in severity_count:
                severity_count[severity] += 1  
            

    print(f'''
    
============================================================
                    SCAN SUMMARY
============================================================

Buckets Scanned : {bucket_count}

Checks Executed : {total_checks}

Passed          : {passed}
Failed          : {failed}
Critical        : {severity_count["CRITICAL"]}
High            : {severity_count["HIGH"]}
Medium          : {severity_count["MEDIUM"]}
Low             : {severity_count["LOW"]}

''')