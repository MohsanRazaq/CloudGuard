markdown# CloudGuard

> **An open-source AWS Cloud Security Misconfiguration Detection and Risk Analysis Platform.**

CloudGuard is a Python-based cloud security scanner that helps identify security misconfigurations in AWS environments before they become security incidents.

The long-term vision is to build an autonomous cloud security platform capable of discovering cloud resources, assessing security posture, prioritizing risks, and providing remediation recommendations.

---

# Current Status

**Version:** v0.2 Security Engine Expansion

### Completed

* AWS SDK (boto3) integration
* Secure IAM user authentication
* AWS session management
* S3 bucket discovery & structural auditing
* Multi-vector S3 security checks (Versioning, Encryption, ACL, PAB, Logging)
* Config-driven scanning matrix
* Execution logging system
* Tiered severity findings generation (`[PASS]`, `[Medium]`, `[High]`)
* Modular project architecture

---

# Current Project Structure

Use code with caution.CloudGuard│├── cloudguard/│   ├── aws/│   ├── security_checks/│   ├── utils/│   ├── findings.py│   └── constants.py│├── docs/├── tests/├── logs/│├── cloudguard.py├── config.json└── README.md
---

# Current Features

## AWS Integration

* Authenticate using IAM credentials
* Create reusable AWS sessions
* Connect securely using low-level `boto3.client` wrappers

## Resource Discovery

* Discover and map all active S3 buckets across the account

## Security Checks

Currently implemented:

* **S3 Bucket Versioning Check**: Inspects and flags disabled or suspended bucket object versioning.
* **S3 Encryption Check**: Assesses object encryption deployment compliance.
* **S3 ACL Review**: Audits legacy Access Control Lists for insecure exposures.
* **S3 Public Access Block (PAB) Check**: Evaluates all 4 strict AWS PAB parameters to block accidental public exposure.
* **S3 Bucket Logging Check**: Validates server access logging infrastructure and identifies missing logging targets.

Upcoming:

* Bucket Policy Analysis (Deep JSON AST parsing)

---

# Example Output

```text
CLOUD GUARD
------------------------------------------------------------
Running Tasks : scan_s3, scan_iam
Skipped Tasks : scan_vpc
------------------------------------------------------------

------------------------------------------------------------
 S3 SECURITY ASSESSMENT
------------------------------------------------------------

[RESOURCE] cloudguard-mohsan-2026
↳ [Medium] versioning: Bucket Versioning Disabled or Suspended
  FIX-> Enable S3 Versioning using s3_client.put_bucket_versioning()
↳ [PASS] Encryption: Secure and compliant
↳ [PASS] ACL: Secure and compliant
↳ [High] Public Access Block: Public Access block is incomplete or disabled
  FIX-> Enable All 4 public Access Block Setting
↳ [High] Bucket Logging: Server access logging is not enabled on this bucket
  FIX-> Configure server access logging using s3_client

------------------------------------------------------------
 SCAN COMPLETE
```

---

# Roadmap

## Phase 1 — S3 Security

* ✅ Bucket Discovery
* ✅ Versioning Check
* ✅ Encryption Check
* ✅ Public Access Check
* ✅ Bucket Logging
* ✅ ACL Analysis
* ⏳ Bucket Policy Review

---

## Phase 2 — IAM Security

* ⏳ MFA Detection
* ⏳ Administrator Access Review
* ⏳ Old Access Keys
* ⏳ Unused Users
* ⏳ Inline Policy Review

---

## Phase 3 — Risk Engine

* ✅ Finding Severity Levels (`[PASS]`, `[Medium]`, `[High]`)
* ⏳ Risk Scoring Engine
* ⏳ Security Summary Dashboard
* ⏳ Compliance Mapping (CIS Benchmarks, OWASP)

---

## Phase 4 — Reporting & Remediation

* ⏳ JSON/HTML Reporting Engines
* ⏳ Executive Summary Exports
* ✅ Actionable Remediation Guidance (`FIX->` Terminal Flags)
* ⏳ Active Auto-Remediation Playbooks

---

# Technology Stack

* Python 3.12+
* Boto3 (AWS SDK for Python)
* AWS IAM
* Amazon S3

---

# Project Goals

* Learn AWS Security Engineering and Architecture
* Build an enterprise-grade open-source cloud security platform
* Apply secure software engineering and strict exception-handling practices
* Maintain a production-style cybersecurity portfolio project

---

# License

This project is open source and intended for educational, auditing, and rese