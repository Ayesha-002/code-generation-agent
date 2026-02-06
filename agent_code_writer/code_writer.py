from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class CodeWriterAgent:
    def __init__(
        self,
        model_name="deepseek-ai/deepseek-coder-1.3b-base",
        max_new_tokens=256,
        temperature=0.2,
    ):
        print("[CodeWriterAgent] Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        print("[CodeWriterAgent] Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="auto"
        )

        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        print("[CodeWriterAgent] Ready.")

    def write_code(self, task: str) -> str:
        prompt = self._build_prompt(task)

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        raw = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        code = self._extract_function(raw)
        return self._strip_non_code(code)


    def _build_prompt(self, task: str) -> str:
        return f"""### Task:
{task}

### Instructions:
Write clean, correct Python code.
Only output code.

### Code:
"""

    def _extract_code(self, text: str) -> str:
        # Simple cleanup for now (will improve later)
        if "### Code:" in text:
            return text.split("### Code:")[-1].strip()
        return text.strip()
    
    def _extract_function(self, text: str) -> str:
        """
        Extracts the first Python function definition from model output.
        """
        lines = text.splitlines()
        function_lines = []
        recording = False

        for line in lines:
            if line.strip().startswith("def "):
                recording = True

            if recording:
                function_lines.append(line)

        return "\n".join(function_lines).strip()
    
    def _strip_non_code(self, text: str) -> str:
        """
        Removes tests, outputs, markdown, and keeps only the function code.
        """
        lines = text.splitlines()
        clean = []
        recording = False

        for line in lines:
            stripped = line.strip()

            # Start recording at function definition
            if stripped.startswith("def "):
                recording = True

            # Stop if tests or output start
            if recording:
                if (
                    stripped.startswith("###")
                    or stripped.startswith(">>>")
                    or stripped.startswith("print")
                ):
                    break
                clean.append(line)

        return "\n".join(clean).strip()
    
    def repair_code(self, original_code: str, issues: list) -> str:
    # 🔒 Clean input first
        original_code = self._strip_non_code(original_code)

        prompt = f"""
    The following Python code has issues:

    ISSUES:
    {issues}

    CODE:
    {original_code}

    INSTRUCTIONS:
    - Fix all issues
    - Do NOT include test code
    - Return ONLY the corrected function
    """

        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        repaired = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 🔒 Clean output before returning
        return self._strip_non_code(self._extract_function(repaired))

