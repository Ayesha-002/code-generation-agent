import subprocess
import sys
from pathlib import Path


class CodeTesterAgent:
    def __init__(self, workspace="workspace"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)

    def run(self, code: str):
        file_path = self.workspace / "generated_code.py"
        file_path.write_text(code, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }