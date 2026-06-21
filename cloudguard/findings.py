class Finding:
    def __init__(
        self,
        resource,
        severity,
        issue,
        recommendation
    ):
        self.resource = resource
        self.severity = severity
        self.issue = issue
        self.recommendation = recommendation

    def __str__(self):
        return (
            f"[{self.severity}] "
            f"{self.resource}: "
            f"{self.issue}"
        )