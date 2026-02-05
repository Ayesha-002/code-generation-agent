from agent_code_writer.code_writer import CodeWriterAgent
from agent_code_writer.code_tester import CodeTesterAgent
from agent_code_writer.code_reviewer import CodeReviewerAgent
from agent_code_writer.code_improver import CodeImproverAgent

writer = CodeWriterAgent()
tester = CodeTesterAgent()
reviewer = CodeReviewerAgent()
improver = CodeImproverAgent(writer)

task = """
Write a Python function that divides two numbers.
Call it with a = 10 and b = 0.
"""

code = writer.write_code(task)

for i in range(3):
    print(f"\n=== ITERATION {i+1} ===")
    print(code)

    result = tester.run(code)

    if result["success"]:
        print("✅ Success")
        print(result["stdout"])
        break

    feedback = reviewer.review(result)
    print("❌ Feedback:", feedback)

    code = improver.improve(code, feedback)