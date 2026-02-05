from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class CodeWriterAgent:
    def __init__(self, model_name="deepseek-ai/deepseek-coder-1.3b-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float32,
            low_cpu_mem_usage=True
        )

    def write_code(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.2,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )