from datetime import datetime
from cloudguard.findings import COLORS 
from cloudguard.utils.logger import feeder
def export_to_html(all_findings, running_tasks):
    findings_list = [finding.to_dict() for finding in all_findings]
    
    table_rows = ""
    for f in findings_list:
        status = f.get('status', 'INFO')
        resource = f.get('resource_id', f.get('resource', 'Unknown'))
        description = f.get('description', f.get('message', 'No details provided'))
        
        bg_color = "#ffebee" if status == "FAIL" else "#e8f5e9"
        text_color = "#c62828" if status == "FAIL" else "#2e7d32"
        
        table_rows += f"""
        <tr>
            <td><span style="background: {bg_color}; color: {text_color}; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{status}</span></td>
            <td><strong>{resource}</strong></td>
            <td>{description}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>CloudGuard Security Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f7fb; color: #333; }}
            .container {{ max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
            .metadata {{ background: #f8fafc; padding: 15px; border-radius: 6px; margin-bottom: 20px; font-size: 0.9em; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            th {{ background: #f1f5f9; color: #475569; }}
            tr:hover {{ background: #f8fafc; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CloudGuard Security Assessment</h1>
            <div class="metadata">
                <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Tasks Executed:</strong> {', '.join(running_tasks)}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Resource</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows if table_rows else "<tr><td colspan='3'>No findings recorded.</td></tr>"}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    report_filename = "cloudguard_report.html"
    with open(report_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
        
    feeder(f"\n{COLORS['GREEN']}HTML report exported successfully to {report_filename}!{COLORS['RESET']}")