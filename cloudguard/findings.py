class Finding:
    def __init__(
        self,
        check,
        resource,
        passed,
        severity,
        issue,
        recommendation
    ):
        self.check=check
        self.resource = resource
        self.passed=passed
        self.severity = severity
        self.issue = issue
        self.recommendation = recommendation

    def __str__(self):
        if self.passed:
            return f"[PASS] {self.check} - {self.resource}"

        return (
        f"[{self.severity}] "
        f"{self.resource}: "
        f"{self.issue}"
    )