class VerifierAgent:
    def verify(self, code: str) -> dict:
        issues = []

        # Rule 1: No test code allowed
        if "print(" in code or "### Test" in code:
            issues.append("Output contains test or print statements")

        # Rule 2: Inefficient prime check
        if "sqrt" not in code and "** 0.5" not in code:
             issues.append("Prime check should iterate till sqrt(n)")

        # Rule 3: Must define function
        if "def " not in code:
            issues.append("No function definition found")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }