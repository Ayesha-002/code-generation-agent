import subprocess
import tempfile
import sys
import os


class ExecutorAgent:
    def run(self, code: str, timeout: int = 5) -> dict:
        """
        Executes Python code safely in a temp file.
        Returns stdout, stderr, and success flag.
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out",
            }

        finally:
            os.remove(tmp_path)