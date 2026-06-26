# CloudGuard

> **An open-source AWS Cloud Security Misconfiguration Detection and Risk Analysis Platform.**

CloudGuard is a Python-based cloud security scanner that helps identify security misconfigurations in AWS environments before they become security incidents.

The long-term vision is to build an autonomous cloud security platform capable of discovering cloud resources, assessing security posture, prioritizing risks, and providing remediation recommendations.

---

# Current Status

**Version:** v0.1 Foundation

### Completed

* AWS SDK (boto3) integration
* Secure IAM user authentication
* AWS session management
* S3 bucket discovery
* S3 bucket versioning security check
* Config-driven scanning
* Logging system
* Basic findings generation
* Modular project architecture

---

# Current Project Structure

```
CloudGuard
│
├── cloudguard/
│   ├── aws/
│   ├── security_checks/
│   ├── utils/
│   ├── findings.py
│   └── constants.py
│
├── docs/
├── tests/
├── logs/
│
├── cloudguard.py
├── config.json
└── README.md
```

---

# Current Features

## AWS Integration

* Authenticate using IAM credentials
* Create reusable AWS sessions
* Connect securely using boto3

## Resource Discovery

* Discover all S3 buckets

## Security Checks

Currently implemented:

* S3 Bucket Versioning

Upcoming:

* Bucket Encryption
* Public Access Block
* Bucket ACL Review
* Bucket Logging
* Bucket Policy Analysis

---

# Example Output

```
============================================================
CloudGuard Scan Started
Running Tasks : scan_s3, scan_iam
Skipped Tasks : scan_vpc
============================================================

=== S3 Discovery ===

[DISCOVERED] cloudguard-mohsan-2026

[Medium]
Bucket Versioning Disabled
```

---

# Roadmap

## Phase 1 — S3 Security

* ✅ Bucket Discovery
* ✅ Versioning Check
* ⏳ Encryption Check
* ⏳ Public Access Check
* ⏳ Bucket Logging
* ⏳ Bucket Policy Review
* ⏳ ACL Analysis

---

## Phase 2 — IAM Security

* MFA Detection
* Administrator Access Review
* Old Access Keys
* Unused Users
* Inline Policy Review

---

## Phase 3 — Risk Engine

* Finding Severity
* Risk Scoring
* Security Summary
* Compliance Mapping

---

## Phase 4 — Reporting

* JSON Reports
* HTML Reports
* Executive Summary
* Remediation Guidance

---

# Technology Stack

* Python 3.12
* boto3
* AWS IAM
* Amazon S3

---

# Project Goals

* Learn AWS Security Engineering
* Build an open-source cloud security platform
* Apply secure software engineering practices
* Build a production-style cybersecurity portfolio project

---

# License

This project is open source and intended for educational and research purposes.
