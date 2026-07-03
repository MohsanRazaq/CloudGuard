# Standard ANSI Terminal Colors
COLORS = {
    "BLUE": "\033[94m",           # Used for Resource names
    "GREEN": "\033[92m",          # Used for [PASS]
    "YELLOW": "\033[93m",         # Used for [Medium] severity
    "RED": "\033[91m",            #Used for [High] severity
    "CYAN": "\033[96m",           # Used for FIX -> recommendations
    "BOLD": "\033[1m",            # Used for Headers
    "RESET": "\033[0m",           # CRITICAL: Resets color back to default white
    "PURPLE": "\033[95m",         # Used for the ISSUE pointer
    "WHITE_BRIGHT": "\033[97m",   # Used for the text of the Issue description
    "GRAY": "\033[90m",           # Used for fallback/alternative severities
    "GREEN_DARK": "\033[32m",     # Used for compliant text message
    "YELLOW_LIGHT": "\033[33m" 
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
        
        sev_val = str(self.severity).upper()
        
        if sev_val == 'HIGH':
            sev_badge = f"{COLORS['RED']}[High]{COLORS['RESET']}"
        elif sev_val == 'MEDIUM':
            sev_badge = f"{COLORS['YELLOW']}[Medium]{COLORS['RESET']}"
        elif sev_val == 'CRITICAL':
            sev_badge = f"{COLORS['PURPLE']}[Medium]{COLORS['RESET']}"
            
        else:
            sev_badge = f"{COLORS['BLUE']}[{self.severity}]{COLORS['RESET']}"

        fix_pointer = f"{COLORS['CYAN']}FIX ->{COLORS['RESET']}"
        issue_pointer = f"{COLORS['CYAN']}ISSUE:{COLORS['RESET']}"
        
        return (
            f"  ↳ {sev_badge} {COLORS['BOLD']}{self.check}{COLORS['RESET']}\n"
            f"      {issue_pointer} {self.issue}\n"
            f"      {fix_pointer} {self.recommendation}"
        )

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "check": self.check,
            "resource": self.resource,
            "passed": self.passed,
            "severity": self.severity if not self.passed else "None",
            "issue": self.issue if not self.passed else "Secure and compliant",
            "recommendation": self.recommendation if not self.passed else "No action required"
        }
