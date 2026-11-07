
from src.ai_planner import plan_test_case
from src.browser_executor import execute_test_case
from src.reporter import generate_report


def main():

    print("\n" + "=" * 55)
    print("AI-POWERED TEST AUTOMATION")
    print("=" * 55)

    instruction = input(
        "\nEnter your test instruction: "
    ).strip()

    if not instruction:
        print("Error: Test instruction cannot be empty.")
        return

    try:
        print("\n[1/3] Generating test plan using Gemini AI...")

        test_case = plan_test_case(instruction)

        print("\nGenerated Test Plan:")
        print("-" * 55)
        print(test_case.model_dump_json(indent=2))

        print("\n[2/3] Executing test using Playwright...")

        report = execute_test_case(
            test_case=test_case,
            headless=False
        )

        print("\n[3/3] Generating execution report...")

        generate_report(report)

    except Exception as error:
        print("\nAUTOMATION ERROR")
        print("=" * 55)
        print(type(error).__name__, error)


if __name__ == "__main__":
    main()
