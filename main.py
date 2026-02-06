from agent_code_writer.code_writer import CodeWriterAgent
from core.executor import ExecutorAgent
from core.verifier_agent import VerifierAgent

MAX_ATTEMPTS = 3

if __name__ == "__main__":
    writer = CodeWriterAgent()
    executor = ExecutorAgent()
    verifier = VerifierAgent()

    task = "Write a Python function that checks if a number is prime."

    code = writer.write_code(task)

    for attempt in range(MAX_ATTEMPTS):
        print(f"\n=== ATTEMPT {attempt + 1} ===\n")
        print(code)

        verification = verifier.verify(code)
        print("\nVerification:", verification)

        if verification["valid"]:
            print("\n✅ Code approved")
            result = executor.run(code)
            print("\n=== EXECUTION RESULT ===")
            print(result)
            break
        else:
            print("\n🔁 Repairing code...")
            code = writer._strip_non_code(code)
    else:
        print("\n❌ Failed to generate valid code after retries")