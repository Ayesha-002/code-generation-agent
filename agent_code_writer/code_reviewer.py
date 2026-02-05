class CodeReviewerAgent:
    def review(self, result: dict) -> str:
        if result["success"]:
            return "Code executed successfully."

        if "ZeroDivisionError" in result["stderr"]:
            return "Division by zero detected. Add input validation."

        return result["stderr"]