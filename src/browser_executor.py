
from playwright.sync_api import sync_playwright

from src.test_schema import TestCase
from src.element_finder import find_element


def execute_test_case(test_case: TestCase, headless=False):

    results = []

    # Give browser interactions a practical minimum timeout.
    def get_timeout(step):
        return max(step.timeout_ms, 30000)

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=headless
        )

        page = browser.new_page()

        try:
            print(f"\nTEST: {test_case.name}")
            print(f"DESCRIPTION: {test_case.description}")
            print("-" * 50)

            for index, step in enumerate(test_case.steps, start=1):

                try:
                    timeout = get_timeout(step)

                    print(f"\nStep {index}: {step.action}")

                    # 1. Navigate
                    if step.action == "navigate":

                        page.goto(
                            step.url,
                            wait_until="domcontentloaded",
                            timeout=max(timeout, 60000)
                        )

                        print(f"Opened: {page.url}")

                    # 2. Wait
                    elif step.action == "wait":

                        page.wait_for_timeout(step.timeout_ms)

                    # 3. Verify page text
                    elif step.action == "assert_text":

                        matching_text = page.get_by_text(
                            step.text,
                            exact=False
                        )

                        matching_text.first.wait_for(
                            state="visible",
                            timeout=timeout
                        )

                        print(f"Verified page text: {step.text}")

                    # 4. Verify page title
                    elif step.action == "assert_title":

                        page.wait_for_function(
                            """expected =>
                                document.title.includes(expected)
                            """,
                            arg=step.text,
                            timeout=timeout
                        )

                        actual_title = page.title()

                        print(f"Actual title: {actual_title}")
                        print(f"Verified page title: {step.text}")

                    # 5. Click or fill an element
                    elif step.action in ["click", "fill"]:

                        element = find_element(
                            page=page,
                            strategy=step.strategy,
                            value=step.value,
                            role=step.role
                        )

                        element.wait_for(
                            state="visible",
                            timeout=timeout
                        )

                        element.scroll_into_view_if_needed(
                            timeout=timeout
                        )

                        if step.action == "click":

                            element.click(
                                timeout=timeout,
                                force=False
                            )

                            print(
                                f"Clicked element: {step.value}"
                            )

                        elif step.action == "fill":

                            element.fill(
                                step.text,
                                timeout=timeout
                            )

                            print(
                                f"Entered text into: {step.value}"
                            )

                    else:
                        raise ValueError(
                            f"Unsupported action: {step.action}"
                        )

                    results.append({
                        "step": index,
                        "action": step.action,
                        "status": "PASS",
                        "error": None
                    })

                    print("Result: PASS")

                except Exception as error:

                    results.append({
                        "step": index,
                        "action": step.action,
                        "status": "FAIL",
                        "error": str(error)
                    })

                    print("Result: FAIL")
                    print("Reason:", error)

                    break

            passed = sum(
                result["status"] == "PASS"
                for result in results
            )

            failed = sum(
                result["status"] == "FAIL"
                for result in results
            )

            overall_status = (
                "PASS" if failed == 0 else "FAIL"
            )

            print("\n" + "=" * 50)
            print("TEST SUMMARY")
            print("=" * 50)
            print("Total executed:", len(results))
            print("Passed:", passed)
            print("Failed:", failed)
            print("Overall result:", overall_status)

            return {
                "test_name": test_case.name,
                "status": overall_status,
                "results": results
            }

        finally:
            print("/nbrowser will remain open for 25 seconds...")
            page.wait_for_timeout(25000)
            browser.close()


if __name__ == "__main__":

    sample_test = TestCase(
        name="Example website title test",
        description="Open a website and verify its page title.",
        steps=[
            {
                "action": "navigate",
                "url": "https://example.com"
            },
            {
                "action": "assert_title",
                "text": "Example Domain"
            }
        ]
    )

    report = execute_test_case(
        test_case=sample_test,
        headless=False
    )
