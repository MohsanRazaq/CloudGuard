# Standard ANSI Terminal Colors
COLORS = {
    "BLUE": "\033[94m",     # Used for Resource names
    "GREEN": "\033[92m",    # Used for [PASS]
    "YELLOW": "\033[93m",   # Used for [Medium] severity
    "RED": "\033[91m",      # Used for [High] severity
    "CYAN": "\033[96m",     # Used for FIX -> recommendations
    "BOLD": "\033[1m",      # Used for Headers
    "RESET": "\033[0m"      # CRITICAL: Resets color back to default white
}


class Finding:
    def __init__(self, check, resource, passed, severity, issue, recommendation):
        self.check = check
        self.resource = resource
        self.passed = passed
        self.severity = severity
        self.issue = issue
        self.recommendation = recommendation

    def __str__(self):
        if self.passed:
            pass_badge = f"{COLORS['GREEN']}[PASS]{COLORS['RESET']}"
            return f"  ↳ {pass_badge} {self.check}: Secure and compliant"
        
        if self.severity == 'HIGH':
            sev_badge = f"{COLORS['RED']}[High]{COLORS['RESET']}"
        elif self.severity == 'MEDIUM':
            sev_badge = f"{COLORS['YELLOW']} Medium{COLORS['RESET']}"
            
        else:
            sev_badge = f"[{self.severity}]"

        
        fix_pointer = f"{COLORS['CYAN']}FIX:{COLORS['RESET']}"
        issue_pointer = f"{COLORS['CYAN']}ISSUE:{COLORS['RESET']}"
        
        return (
            f"  ↳ {sev_badge} {COLORS['BOLD']}{self.check}{COLORS['RESET']}"
            f"\n           {issue_pointer} {self.issue}\n"
            f"            {fix_pointer} {self.recommendation}"
        )

