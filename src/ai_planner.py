
import os
import json
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.test_schema import TestCase


# Load environment variables from .env
load_dotenv()


def is_retryable_error(error):
    """Identify temporary Gemini API errors."""

    error_message = str(error).lower()

    retryable_statuses = [
        "429",
        "500",
        "502",
        "503",
        "504"
    ]

    return any(
        status in error_message
        for status in retryable_statuses
    )


def generate_with_retry(
    client,
    model_name,
    prompt,
    max_attempts=3
):
    """Retry Gemini requests when temporary server errors occur."""

    for attempt in range(1, max_attempts + 1):

        try:
            return client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TestCase,
                    temperature=0.1
                )
            )

        except Exception as error:

            if (
                not is_retryable_error(error)
                or attempt == max_attempts
            ):
                raise

            delay = 2 ** attempt

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {delay} seconds "
                f"({attempt}/{max_attempts - 1})..."
            )

            time.sleep(delay)


def plan_test_case(user_instruction: str) -> TestCase:
    """
    Convert a plain-English instruction into
    a structured browser automation test.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Check your .env file."
        )

    if not user_instruction.strip():
        raise ValueError(
            "Test instruction cannot be empty."
        )

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            api_version="v1beta"
        )
    )

    prompt = f"""
You are an expert browser test automation planner.

Convert the user's plain-English instruction into
a structured browser automation test.

USER INSTRUCTION:
{user_instruction}

SUPPORTED ACTIONS:
- navigate
- click
- fill
- assert_text
- assert_title
- wait

RULES:

1. Return a test plan matching the supplied response schema.

2. For navigate:
   Provide a complete URL starting with http:// or https://.

3. For click:
   You MUST provide all three fields:
   - strategy: "role"
   - role: the element's accessible role
   - value: the element's accessible name

   IMPORTANT:
   - The field name MUST be "value".
   - Never use "text" instead of "value".
   - Never omit the value field.
   - Never set value to null.

   Example:
   {{
     "action": "click",
     "strategy": "role",
     "role": "button",
     "value": "Submit"
   }}

4. For fill:
   You MUST provide:
   - strategy: "label" or "role"
   - value: the exact label or accessible name of the input
   - text: the exact text to enter

   Example:
   {{
     "action": "fill",
     "strategy": "label",
     "value": "Text input",
     "text": "CloudQA test"
   }}

5. For assert_text:
   Put the expected visible page text in the text field.
   Do not provide a locator strategy or value.

6. For assert_title:
   Put the expected page title in the text field.

7. For wait:
   Use timeout_ms as the waiting duration.

8. Use 5000 as the default timeout_ms for other actions.

9. Never invent URLs, credentials, selectors, or expected results.

10. Do not generate executable Python or JavaScript code.

11. Do not add actions that the user did not request.
"""

    try:
        print("Sending test instruction to Gemini...")

        response = generate_with_retry(
            client=client,
            model_name=model_name,
            prompt=prompt
        )

        # Parse Gemini response
        if response.text:

            data = json.loads(response.text)

        elif response.parsed is not None:

            if isinstance(response.parsed, TestCase):
                data = response.parsed.model_dump()

            elif isinstance(response.parsed, dict):
                data = response.parsed

            else:
                raise ValueError(
                    "Gemini returned an unexpected response format."
                )

        else:
            raise ValueError(
                "Gemini returned an empty response."
            )

        # Recover missing button names from the original instruction
        for step in data.get("steps", []):

            if (
                step.get("action") == "click"
                and not step.get("value")
            ):

                match = re.search(
                    r"""\bbutton\s+(?:named|called|labelled|labeled)\s+["']([^"']+)["']""",
                    user_instruction,
                    re.IGNORECASE
                )

                if match:

                    step["value"] = match.group(1)

                    print(
                        "Recovered missing button name:",
                        step["value"]
                    )

                else:
                    raise ValueError(
                        "Gemini generated a click action "
                        "without a button name. Please specify "
                        "the button name in your instruction."
                    )

        # Validate the complete test plan
        test_case = TestCase.model_validate(data)

        return test_case

    finally:
        client.close()


if __name__ == "__main__":

    print("\nStarting Gemini AI Planner...")
    print("=" * 50)

    instruction = (
        "Open https://example.com and verify that "
        "the page title is Example Domain."
    )

    try:
        test_case = plan_test_case(instruction)

        print("\nGENERATED TEST PLAN")
        print("=" * 50)

        print(
            test_case.model_dump_json(indent=2)
        )

        print("\nAI planning completed successfully!")

    except Exception as error:

        print("\nAI PLANNER ERROR")
        print("=" * 50)

        print(type(error).__name__, error)
