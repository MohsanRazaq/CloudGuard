from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# CloudGuard Core Imports
from cloudguard.aws.s3_scanner import list_buckets
from cloudguard.aws.session import create_session
from cloudguard.utils.config_loader import load_config
from plugin_manager import PluginRegistry, load_all_plugins

# Page Setup
st.set_page_config(
    page_title="CloudGuard Security", page_icon="🛡️", layout="wide"
)

st.title("🛡️ CloudGuard Security Assessment Dashboard")
st.markdown(
    "Scan and monitor your AWS cloud security configurations in real time."
)

# Sidebar Configuration
st.sidebar.header("Scan Setup")

# Load Configuration
try:
    config = load_config()
except Exception:
    config = {"s3": True, "iam": True}  # Fallback default

st.sidebar.subheader("Tasks Configuration Status")
for task, enabled in config.items():
    status = "Enabled" if enabled else "Disabled"
    st.sidebar.text(f"{task.upper()}: {status}")

# Trigger Scan Execution
if st.sidebar.button("🚀 Run Cloud Security Scan", type="primary"):
    with st.spinner("Scanning AWS Environment. Please wait..."):
        start_time = datetime.now()

        # Initialize Session & Plugin Registry
        session = create_session()
        s3_client = session.client("s3")
        registry = PluginRegistry()
        load_all_plugins(registry)

        buckets = list_buckets(s3_client) or []
        bucket_count = len(buckets)

        all_findings = []
        context = {"session": session, "s3_client": s3_client}

        # Filter registered S3 plugins dynamically
        s3_plugins = [
            plugin
            for plugin in registry._registry.values()
            if "s3" in [s.lower() for s in plugin.supported_services]
        ]

        # Execute registered plugins against all discovered buckets
        for plugin in s3_plugins:
            try:
                findings_list = plugin.execute(context)
                for finding in findings_list:
                    # Support both Finding objects and raw dicts
                    if hasattr(finding, "to_dict"):
                        all_findings.append(finding.to_dict())
                    elif isinstance(finding, dict):
                        all_findings.append(finding)
            except Exception as e:
                st.error(f"Error executing plugin {plugin.name}: {e}")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

    st.success("Scan Completed!")

    # Top Metric Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Buckets Scanned", bucket_count)
    col2.metric("Total Findings Detected", len(all_findings))
    col3.metric("Scan Execution Time", f"{duration:.2f} seconds")

    # Render Charts and Table Results
    if all_findings:
        df = pd.DataFrame(all_findings)

        st.subheader("📊 Assessment Findings Distribution")

        # Determine best column for pie chart breakdown
        status_column = None
        for col in ["passed", "severity", "status", "check"]:
            if col in df.columns:
                status_column = col
                break

        if status_column:
            chart_col, data_col = st.columns([1, 2])

            with chart_col:
                status_counts = df[status_column].value_counts()

                fig, ax = plt.subplots(figsize=(4, 4))
                ax.pie(
                    status_counts,
                    labels=[str(lbl) for lbl in status_counts.index],
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#ff4b4b", "#00c0f2", "#ffbd45", "#2e7d32"][
                        : len(status_counts)
                    ],
                )
                ax.axis("equal")
                st.pyplot(fig)

            with data_col:
                st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

        # JSON Export Download Option
        st.subheader("📥 Export Assessment Data")
        json_report = df.to_json(orient="records", indent=4)

        st.download_button(
            label="⬇ Download CloudGuard JSON Report",
            data=json_report,
            file_name=f"cloudguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )
    else:
        st.info(
            "✨ No security vulnerabilities or findings were detected on your S3 buckets."
        )