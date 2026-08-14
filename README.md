![Tests](https://github.com/MohsanRazaq/CloudGuard/actions/workflows/tests.yml/badge.svg)
#  CloudGuard

> An extensible cloud security scanner for identifying cloud misconfigurations and generating actionable security reports.

**Current Provider:** Amazon Web Services (AWS)  
**Current Services:** Amazon S3, AWS IAM, Dynamic Plugin Engine

CloudGuard is an open-source cloud security assessment tool designed to help developers, cloud engineers, and security professionals discover insecure cloud configurations before deployment. The project currently focuses on Amazon S3 security assessments and is built with a modular architecture that can be extended to additional AWS services and other cloud providers in future releases.

## Why CloudGuard?

Cloud environments are powerful but can become difficult to secure as infrastructure grows. Simple configuration mistakes—such as disabled encryption, missing versioning, or publicly accessible buckets—can lead to security incidents, compliance violations, and unnecessary audit costs.

CloudGuard helps identify these issues automatically by scanning cloud resources and producing clear, actionable security findings.

Instead of overwhelming users with raw API responses, CloudGuard presents:

- Actionable security findings
- Risk-based severity levels
- Security score
- Scan summaries
- JSON reports for automation

##  Project Status

CloudGuard is currently under active development.

### Implemented

- Dynamic Plugin Engine
- Automatic Plugin Discovery
- Plugin Registry
- Plugin Interface Architecture
- AWS S3 Security Assessment
- Bucket Versioning Check
- Bucket Encryption Check
- Bucket ACL Review
- Bucket Policy Analysis
- Public Access Block Validation
- Server Access Logging Check
- AWS IAM Security Assessment
- IAM MFA Audit
- IAM Access Key Audit
- Security Score Calculation
- Risk Classification
- HTML Report Generator
- JSON Report Export
- Colorized CLI Output
- Streamlit Dashboard
- Pytest Test Suite
- GitHub Actions CI
- Improved HTML Reports
- IAM_user_mfa
- Implemented Well individual and total risk score for better Risk calculations

###  In Progress
- IAM Security Assessment
- Advanced Security Scoring
- Additional Unit Tests

###  Planned

- CloudTrail Validation
- EC2 Security Checks
- Security Group Analysis
- EBS Encryption Checks
- Azure Support
- Google Cloud Support

##  Features

###  Security Assessment

CloudGuard currently performs automated security assessments for Amazon S3 buckets, including:

- ✅ Bucket Versioning validation
- ✅ Server-Side Encryption verification
- ✅ Bucket ACL (Access Control List) review
- ✅ Public Access Block validation
- ✅ Bucket Policy analysis
- ✅ Server Access Logging verification

---

###  Security Reporting

After each scan, CloudGuard generates:

- Risk-weighted Security Score
- Overall Risk Level (Low / Medium / High)
- Colorized terminal output
- Bucket-wise security findings
- Severity classification (Critical, High, Medium, Low)
- Actionable remediation recommendations
- JSON report export for automation and further analysis

---

###  Modular Architecture

CloudGuard is designed to be easily extended.
---
                 CLI / Dashboard
                        │
                        ▼
                 Scan Engine
                        │
                        ▼
              Plugin Manager
                        │
      ┌─────────────────┼────────────────ti─┐
      ▼                 ▼                 ▼
   S3 Plugins      IAM Plugins      Future Plugins
      │                 │
      └────────────┬────┘
                   ▼
            Finding Engine
                   │
                   ▼
           HTML / JSON / CLI

           ---

Current modules include:

- AWS Session Management
- S3 Resource Discovery
- Independent Security Check Modules
- Findings Engine
- Reporting Engine
- Logging Utilities
- Configuration Loader

This modular architecture allows new security checks and cloud services to be added with minimal code changes.

---
### Plugin Engine

- Dynamic Plugin Discovery
- Automatic Plugin Registration
- Plugin Interface
- Plugin Registry
- Runtime Plugin Loading
- Service-based Plugin Organization


##  Dynamic Plugin System

CloudGuard now uses a dynamic plugin architecture that automatically discovers and loads security plugins at runtime.

Every plugin implements a common `PluginInterface`, allowing new security checks to be added without modifying the core scan engine.

### Benefits

- Automatic plugin discovery
- Extensible architecture
- Decoupled scan engine
- Easy feature development
- Independent security modules
- Future support for AWS, Azure and GCP plugins

---


###  Configuration

CloudGuard supports configurable scanning through `config.json`.

Current configurable scan modules include:

- `scan_s3`
- `scan_iam`
- `scan_vpc`

Additional modules will be supported as development continues.

---

###  Future Expansion

CloudGuard is being developed as a multi-cloud security assessment platform.

Planned support includes:

- AWS IAM
- AWS CloudTrail
- AWS EC2
- AWS Security Groups
- AWS EBS
- AWS KMS
- Azure
- Google Cloud Platform (GCP)

##  Architecture

CloudGuard follows a modular architecture where each component has a single responsibility. This makes the scanner easy to maintain, test, and extend with additional cloud services and security checks.

```
                   +----------------------+
                   |      CloudGuard      |
                   |    (cloudguard.py)   |
                   +----------+-----------+
                              |
             +----------------+----------------+
             |                                 |
             ▼                                 ▼
    +----------------+               +----------------+
    |  AWS Session   |               | Configuration  |
    | (boto3 Client) |               |  config.json   |
    +-------+--------+               +----------------+
            |
            ▼
    +----------------------+
    |  Resource Discovery  |
    |     S3 Buckets       |
    +----------+-----------+
               |
               ▼
    +---------------------------------------------+
    |           Security Check Engine             |
    +---------------------------------------------+
      |        |         |        |        |       |
      ▼        ▼         ▼        ▼        ▼       ▼
 Version   Encryption   ACL   Public   Logging  Policy
                              Block

               |
               ▼
       +------------------+
       | Finding Objects  |
       +------------------+
               |
               ▼
      +---------------------+
      | Reporting Engine    |
      +---------------------+
        |               |
        ▼               ▼
 CLI Summary      JSON Report
```

### Core Components

| Module | Responsibility |
|---------|----------------|
| **AWS Session** | Creates authenticated boto3 clients |
| **Resource Discovery** | Discovers AWS resources for scanning |
| **Security Checks** | Executes independent security validation modules |
| **Finding Engine** | Represents scan results in a consistent format |
| **Reporting Engine** | Generates terminal summaries and JSON reports |
| **Logger** | Stores scan logs for auditing and troubleshooting |
| **Configuration Loader** | Enables or disables scan modules using `config.json` |

### Design Principles

CloudGuard is built around several engineering principles:

- Modular architecture
- Single Responsibility Principle (SRP)
- Extensible security check framework
- Separation of scanning and reporting logic
- Reusable Finding model
- Configurable scan execution

# 🚀 Quick Start

## Prerequisites

Before running CloudGuard, ensure you have:

- Python **3.10+**
- An AWS account
- AWS CLI configured with valid credentials
- Internet connection

---

## Clone the Repository

```bash
git clone https://github.com/MohsanRazaq/CloudGuard.git
cd CloudGuard
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure AWS Credentials
## Environment Configuration (LocalStack vs. Real AWS)

CloudGuard supports testing locally via **LocalStack** or scanning a **Live AWS Account** using a single configuration switch in `.env`.

### 1. Create a `.env` File
Create a `.env` file in the project root directory:

```env
# Set to 'true' for LocalStack, 'false' for Real AWS
USE_LOCALSTACK=false

# LocalStack Gateway Endpoint
LOCALSTACK_ENDPOINT=http://localhost:4566

# Default AWS Region
AWS_DEFAULT_REGION=us-east-1

Security Notice: Do not place real AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY inside .env to prevent accidental credential leakage in Git repositories

##Execution Modes
#Scan Live AWS Account
Export your temporary or IAM credentials directly into your terminal environment, then launch the scan
```bash
# Set credentials in environment
export AWS_ACCESS_KEY_ID="AKIAXXXXXXXXXXXXXXXX"
export AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AWS_DEFAULT_REGION="us-east-1"

# Run CloudGuard scan
python3 cloudguard.py --scan
```
```
#Scan Offline via LocalStack

Ensure your LocalStack Docker container is running, set USE_LOCALSTACK=true in .env, and execute with mock credentials:
```bash
# Ensure container is up
docker ps

# Run scan using LocalStack endpoint
AWS_ENDPOINT_URL="http://localhost:4566" 
AWS_ACCESS_KEY_ID="test" 
AWS_SECRET_ACCESS_KEY="test" 
python3 cloudguard.py --scan
```
```
CloudGuard uses the default AWS credential chain provided by **boto3**.

If AWS CLI is not configured, run:

```bash
aws configure
```

Provide:

```
AWS Access Key ID
AWS Secret Access Key
Default Region
Output Format (json)
```

CloudGuard automatically uses these credentials during the scan.

---

## Configure Scan Modules

Edit `config.json` to enable or disable scan modules.

Example:

```json
{
    "scan_s3": true,
    "scan_iam": false
}
```

---

## Run CloudGuard

```bash
python cloudguard.py
```

---

##  Why I Built CloudGuard

CloudGuard was created as a hands-on cloud security project to deepen my understanding of AWS security services and secure software design.

Rather than relying solely on existing security tools, I wanted to build a scanner from scratch to understand how cloud security assessments work internally—from AWS API interactions to finding generation and reporting.

The long-term vision is to evolve CloudGuard into a modular multi-cloud security assessment platform supporting AWS, Azure, and Google Cloud.

## Example Output

```text
CLOUD GUARD

Running Tasks : scan_s3

------------------------------------------------------------
S3 SECURITY ASSESSMENT
------------------------------------------------------------

[RESOURCE] cloudguard-example

↳ [Medium] Versioning
↳ [PASS] Encryption
↳ [High] Public Access Block
↳ [PASS] Bucket ACL

============================================================
SCAN SUMMARY
============================================================

Security Score : 82/100
Risk Level     : MEDIUM
Buckets Scanned: 5
```
## How the Security Score is Calculated

Every scan starts at a perfect score of 100. Points are deducted for each
failed security check, weighted by severity:

| Severity | Points deducted per finding |
|----------|------------------------------|
| Critical | 25 |
| High     | 10 |
| Medium   | 5  |
| Low      | 2  |

The final score determines the overall risk level:

| Score range | Risk level |
|-------------|------------|
| 90–100      | LOW RISK |
| 70–89       | MEDIUM RISK |
| Below 70    | HIGH RISK |

The score is capped at a minimum of 0 — a resource with many critical
findings will show as 0/100 rather than a negative number.

## ✅ Tested Environment

| Component | Version |
|-----------|---------|
| Python | 3.12 |
| Ubuntu | 24.04 LTS |
| boto3 | Latest |
| AWS CLI | v2 |

# 📂 Project Structure

```text
CloudGuard/
├── cloudguard.py
├── plugin_manager.py
├── config.json
├── requirements.txt
├── cloudguard/
│   ├── aws/
│   ├── engine/
│   ├── reporting/
│   ├── findings.py
│   └── utils/
├── plugins/
│   ├── s3/
│   └── iam/
├── dashboard/
└── tests/
```

---

## Directory Overview

| Directory | Purpose |
|-----------|----------|
| **aws/** | AWS authentication and resource discovery |
| **security_checks/** | Independent security validation modules |
| **reporting/** | CLI summaries and report generation |
| **utils/** | Logging and configuration helpers |
| **tests/** | Unit tests for security checks |
| **logs/** | Scan logs |
| **docs/** | Documentation and screenshots |

#  How CloudGuard Works

CloudGuard follows a simple scanning pipeline.

```
Start Scan
    │
    ▼
Load Configuration
    │
    ▼
Create AWS Session
    │
    ▼
Discover Resources
    │
    ▼
Execute Security Checks
    │
    ▼
Generate Findings
    │
    ▼
Calculate Security Score
    │
    ▼
Generate Reports
    │
    ├── Terminal Report
    └── JSON Report
```

Each security check runs independently and returns a standardized `Finding` object.

This modular design allows new security checks and cloud services to be added without modifying the core scanning engine.


##  Example JSON Report

```json
{
  "scan_metadata": {
    "engine": "CloudGuard",
    "version": "v1.0.0",
    "timestamp": "2026-07-04 00:57:59",
    "tasks_run": [
      "scan_s3"
    ]
  },
  "findings": [
    {
      "check": "Public Access Block",
      "resource": "cloudguard-learning-bucket-test",
      "passed": false,
      "severity": "HIGH",
      "issue": "Public Access block is incomplete or disabled",
      "recommendation": "Enable All 4 public Access Block Setting"
    }
  ]
}
```

CloudGuard exports a complete JSON report that can be integrated with dashboards, CI/CD pipelines, or other automation workflows.

#  Roadmap

## Version 0.2

- [x] HTML Report Generation
- [-] CSV Report Export
- [-] Enhanced Risk Scoring Engine
- [-] Expand Unit Test Coverage
- [x] Automated Testing with GitHub Actions (CI)

## Version 0.3

- [x] IAM Security Assessment
- [ ] CloudTrail Security Checks
- [ ] EC2 Security Assessment
- [ ] Security Group Analysis

## Version 0.4

- [ ] Multi-Region Scanning
- [ ] Multi-Account Support
- [ ] Docker Support
- [ ] GitHub Actions CI

## Version 1.0

- [ ] Azure Support
- [ ] Google Cloud Platform Support
- [x] Plugin System
- [x] Web Dashboard


# Screenshots

## CloudGuard Scan

Displays discovered resources, security findings, and remediation recommendations.

![CloudGuard Scan](docs/images/cloudguard_scan.png)

---

## Scan Summary

Displays security score, scan duration, severity breakdown, and overall risk level.

![Scan Summary](docs/images/scan_summary.png)

---

## JSON Report

CloudGuard exports machine-readable JSON reports for automation and integration.

![JSON Report](docs/images/json_report.png)

#  Current Security Checks

| Check | Status |
|--------|--------|
| Bucket Versioning | ✅ |
| Bucket Encryption | ✅ |
| Bucket ACL Review | ✅ |
| Public Access Block | ✅ |
| Bucket Logging | ✅ |
| Bucket Policy | ✅ |
| Security Score | ✅ |
| JSON Report | ✅ |
| CLI Summary | ✅ |

#  Project Metrics

- Programming Language: Python
- Cloud Provider: AWS
- Services Supported: Amazon S3,IAM
- Security Checks: 8+
- Report Formats: CLI, HTML, JSON
- Architecture: Plugin-Based Modular


# Next Implementations Quequed:

 -IAM Checks[5]
 -EC2 checks[5]

#  Contributing

Contributions are welcome!

If you'd like to improve CloudGuard:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

Bug reports, feature requests, and security suggestions are always appreciated.

#  License

This project is licensed under the MIT License.

#  Acknowledgements

CloudGuard is built using:

- AWS SDK for Python (boto3)
- Python
- AWS Documentation
