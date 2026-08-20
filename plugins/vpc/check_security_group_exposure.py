from plugin_manager import PluginInterface
from cloudguard.findings import Finding
from cloudguard.constants import PORTS
from rich import print


class Plugin(PluginInterface):
    # --- METADATA PROPERTIES ---
    @property
    def name(self) -> str:
        return "VPC Security Group Exposure Check"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def author(self) -> str:
        return "Mohsan"

    @property
    def description(self) -> str:
        return "Check the exposure of VPC Security Groups."

    @property
    def category(self) -> str:
        return "EC2"

    @property
    def supported_services(self) -> list:
        return ["vpc"]

    @property
    def default_severity(self) -> str:
        return "HIGH"

    @property
    def dependencies(self) -> list:
        return []

    # --- EXECUTION ENGINE ---
    def execute(self, context: dict) -> list:
        ec2_client = context.get("ec2") or context["session"].client('ec2')

        return self.get_all_security_groups(ec2_client)



    def get_all_security_groups(self,ec2_client)->list:
        sg_audit=ec2_client.describe_security_groups().get("SecurityGroups",[])
        findings=[]

        for sg in sg_audit:
            sg_id=sg.get("GroupId",'')
            sg_name=sg.get("GroupName",'')
            inbound_rules=sg.get("IpPermissions",[])
            # iteration through each Security Rule
            for rule in inbound_rules:
                ip_protocol=rule.get("IpProtocol",'')
                from_port=rule.get("FromPort")
                to_port=rule.get("ToPort")
                # get all cidrs
                ipv4_sources=[r.get("CidrIp") for r in rule.get("IpRanges",[])]
                ipv6_sources=[r.get("CidrIpv6") for r in rule.get("Ipv6Ranges",[])]
                is_public='0.0.0.0/0' in ipv4_sources or '::/0' in ipv6_sources
                is_all_traffic=ip_protocol=='-1'
                matched_ports=[]
                if ip_protocol=='tcp' and from_port is not None and to_port is not None:
                    matched_ports=[p for p in PORTS if  from_port<=p<=to_port]
                if is_public and (is_all_traffic or matched_ports):
                    
                    findings.append(
                        Finding(
                            check="Security Group Exposure",
                            category="VPC",
                            resource=f"SecurityGroupId: {sg_id} [{sg_name}]",
                            passed=False,
                            severity="CRITICAL",
                            issue=f"Exposed PORTS {matched_ports if not is_all_traffic else 'All ports 0-65635'}",
                            recommendation="Restrict inbound SSH access to trusted source IPs and avoid exposing port 22 to 0.0.0.0/0 or ::/0 unless required",
                            ))
                        
            
        return findings

                        
                                
    
