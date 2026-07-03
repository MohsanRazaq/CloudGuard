from cloudguard.findings import COLORS
from rich.console import Console
from rich.progress_bar import ProgressBar
def print_summary(findings, bucket_count, start, end):
    severity_count = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }
    
    total_checks = len(findings)
    score = 100
    passed = 0
    failed = 0

    for finding in findings:
        if finding.passed:
            passed += 1
        else:
            failed += 1
            
            
            severity = finding.severity
            
            
            if severity in severity_count:
                severity_count[severity] += 1  

    critical_weightage=severity_count['CRITICAL']*25 if severity_count['CRITICAL']>0 else 0          
    high_weightage=severity_count['HIGH']*10         if severity_count['HIGH']>0 else 0       
    medium_weightage=severity_count['MEDIUM']*5      if severity_count['MEDIUM']>0 else 0       
    low_weightage=severity_count['LOW']*2            if severity_count['LOW']>0 else 0       
    total_pass=critical_weightage+high_weightage+low_weightage+medium_weightage    
    score-=total_pass


    if score >= 90:
        risk_level = f"{COLORS['GREEN']}LOW RISK{COLORS['RESET']}"
    elif score >= 70:
        risk_level = f"{COLORS['YELLOW']}MEDIUM RISK{COLORS['RESET']}"
    else:
        risk_level = f"{COLORS['RED']}HIGH RISK{COLORS['RESET']}"
    

    print(f'''
============================================================
                    {COLORS['GREEN']}SCAN SUMMARY{COLORS['RESET']}
                    {COLORS['GREEN']}CloudGuard v1.0.0{COLORS['RESET']}
            Start: {start.strftime('%I:%M:%S %p')} | End: {end.strftime('%I:%M:%S %p')}
============================================================
Total Scan Time : {COLORS['BOLD']}{(end - start).total_seconds():.2f}s{COLORS['RESET']}
Security Score  : {score}/100
Risk level      : {risk_level}

Buckets Scanned : {bucket_count}
Checks Executed : {total_checks}
Passed          : {passed}
Failed          : {failed}

Critical        : {COLORS['RED']}{severity_count["CRITICAL"]}{COLORS['RESET']}
High            : {COLORS['GREEN']}{severity_count["HIGH"]}{COLORS['RESET']}
Medium          : {COLORS['YELLOW']}{severity_count["MEDIUM"]}{COLORS['RESET']}
Low             : {COLORS['WHITE_BRIGHT']}{severity_count["LOW"]}{COLORS['RESET']}
''')
