import ast

class VerifierAgent:
    def verify(self, code: str) -> dict:
        issues = []

        # 1️⃣ Syntax check
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {"valid": False, "issues": ["Syntax error in code"]}

        # 2️⃣ Exactly one function
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if len(functions) != 1:
            issues.append("Code must contain exactly one function")

        # 3️⃣ No print statements
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "print":
                issues.append("Output contains print statements")

        # 4️⃣ Must return something
        if not any(isinstance(n, ast.Return) for n in ast.walk(tree)):
            issues.append("Function must return a value")

        # 5️⃣ Algorithmic quality checks (prime-specific)
        code_lower = code.lower()

        if "is_prime" in code_lower:
            if "** 0.5" not in code_lower and "sqrt" not in code_lower:
                issues.append("Prime check is inefficient; should loop till sqrt(n)")

            if "n < 2" not in code_lower and "number < 2" not in code_lower:
                issues.append("Prime check should handle numbers less than 2")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
