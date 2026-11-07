
def generate_report(report):
    """Display the browser test execution report."""

    print("\n" + "=" * 55)
    print("TEST EXECUTION REPORT")
    print("=" * 55)

    print("Test Name:", report.get("test_name", "Unknown"))
    print("Overall Status:", report.get("status", "UNKNOWN"))

    results = report.get("results", [])

    print("\nSTEP DETAILS")
    print("-" * 55)

    for result in results:
        print(
            f"\nStep {result.get('step', '?')}: "
            f"{result.get('action', 'Unknown')}"
        )

        print("Status:", result.get("status", "UNKNOWN"))

        error = result.get("error")

        if error:
            print("Error:", error)

    passed = sum(
        item.get("status") == "PASS"
        for item in results
    )

    failed = sum(
        item.get("status") == "FAIL"
        for item in results
    )

    print("\n" + "-" * 55)
    print("Total executed:", len(results))
    print("Passed:", passed)
    print("Failed:", failed)
    print("Final result:", report.get("status", "UNKNOWN"))
    print("=" * 55)
