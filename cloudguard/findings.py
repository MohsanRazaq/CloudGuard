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
            return f"↳ [PASS] {self.check}: Secure and compliant"

        return (
            f"↳ [{self.severity}] {self.check}: {self.issue}\n"
            f"  FIX-> {self.recommendation}"
        )
