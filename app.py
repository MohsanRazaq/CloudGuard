import streamlit as st
import pandas as pd
from datetime import datetime

# imports
from cloudguard.utils.config_loader import load_config
from cloudguard.aws.session import create_session
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.security_checks.check_bucket_versioning import check_bucket_versioning
from cloudguard.security_checks.check_bucket_encryption import check_bucket_encryption
from cloudguard.security_checks.check_bucket_public_block import check_public_access_block
from cloudguard.security_checks.check_bucket_logging import check_bucket_logging
from cloudguard.security_checks.check_bucket_acl import check_bucket_acl
from cloudguard.security_checks.check_bucket_policy import check_bucket_policy

# S3 Check mappings
S3_SECURITY_CHECKS = [
    check_bucket_versioning,
    check_bucket_encryption,
    check_public_access_block,
    check_bucket_logging,
    check_bucket_acl,
    check_bucket_policy
]


st.set_page_config(page_title="CloudGuard Security", page_icon="🛡️", layout="wide")


st.title("CloudGuard Security Assessment Dashboard")
st.markdown("Scan and monitor your AWS cloud security configurations in real time.")

st.sidebar.header("Scan Setup")
config = load_config()

st.sidebar.subheader("Tasks Configuration Status")
for task, enabled in config.items():
    status = "Enabled" if enabled else "Disabled"
    st.sidebar.text(f"{task.upper()}: {status}")

if st.sidebar.button(" Run Cloud Security Scan", type="primary"):
    with st.spinner("Scanning AWS Environment .Please wait..."):
        start_time = datetime.now()
        
        session = create_session()
        s3_client = session.client('s3')
        buckets = list_buckets(s3_client)
        bucket_count = len(buckets)
        
        all_findings = []
        
        for bucket in buckets:
            for check in S3_SECURITY_CHECKS:
                result = check(bucket, s3_client)
                all_findings.append(result.to_dict())
                
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
    
    st.success("Scan Completed!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Buckets Scanned", bucket_count)
    col2.metric("Total Findings Detected", len(all_findings))
    col3.metric("Scan Execution Time", f"{duration:.2f} seconds")
    
    if all_findings:
        df = pd.DataFrame(all_findings)
        
        st.subheader(" Assessment Findings Distribution")
        
        status_column = 'status' if 'status' in df.columns else (df.columns[2] if len(df.columns) > 2 else None)
        
        if status_column:
            chart_col, data_col = st.columns([1, 2])
            with chart_col:
                status_counts = df[status_column].value_counts()
                # Native streamline alternative that works without configurations
                st.bar_chart(status_counts)


            with data_col:
                st.dataframe(df, width='content')
        else:
            st.dataframe(df, width='content')
            
        st.subheader(" Export Assessment Data")
        json_report = df.to_json(orient="records", indent=4)
        
        st.download_button(
            label="⬇ Download CloudGuard JSON Report",
            data=json_report,
            file_name=f"cloudguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    else:
        st.info(" No security vulnerabilities or findings were detected on your S3 buckets.")
