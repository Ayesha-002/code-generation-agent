class CodeImproverAgent:
    def __init__(self, writer):
        self.writer = writer

    def improve(self, code: str, feedback: str) -> str:
        prompt = f"""
Fix the following Python code.

CODE:
{code}

ISSUE:
{feedback}

Return only the corrected code.
"""
        return self.writer.write_code(prompt)