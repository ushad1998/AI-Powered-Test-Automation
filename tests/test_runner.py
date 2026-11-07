
import unittest
from pydantic import ValidationError

from src.test_schema import TestAction, TestCase


class TestActionValidation(unittest.TestCase):

    def test_valid_navigation(self):
        step = TestAction(
            action="navigate",
            url="https://example.com"
        )
        self.assertEqual(step.action, "navigate")

    def test_invalid_navigation_url(self):
        with self.assertRaises(ValidationError):
            TestAction(
                action="navigate",
                url="example.com"
            )

    def test_navigation_requires_url(self):
        with self.assertRaises(ValidationError):
            TestAction(action="navigate")

    def test_valid_fill_action(self):
        step = TestAction(
            action="fill",
            strategy="label",
            value="Email",
            text="test@example.com"
        )
        self.assertEqual(step.text, "test@example.com")

    def test_fill_requires_text(self):
        with self.assertRaises(ValidationError):
            TestAction(
                action="fill",
                strategy="label",
                value="Email"
            )

    def test_click_requires_locator(self):
        with self.assertRaises(ValidationError):
            TestAction(action="click")

    def test_role_strategy_requires_role(self):
        with self.assertRaises(ValidationError):
            TestAction(
                action="click",
                strategy="role",
                value="Submit"
            )

    def test_default_timeout(self):
        step = TestAction(
            action="navigate",
            url="https://example.com"
        )
        self.assertEqual(step.timeout_ms, 5000)

    def test_zero_timeout_uses_default(self):
        step = TestAction(
            action="navigate",
            url="https://example.com",
            timeout_ms=0
        )
        self.assertEqual(step.timeout_ms, 5000)

    def test_timeout_cannot_exceed_limit(self):
        with self.assertRaises(ValidationError):
            TestAction(
                action="navigate",
                url="https://example.com",
                timeout_ms=70000
            )

    def test_valid_assert_text(self):
        step = TestAction(
            action="assert_text",
            text="Welcome"
        )
        self.assertEqual(step.text, "Welcome")


class TestCaseValidation(unittest.TestCase):

    def test_valid_test_case(self):
        test_case = TestCase(
            name="Example test",
            description="Verify example website",
            steps=[
                {
                    "action": "navigate",
                    "url": "https://example.com"
                }
            ]
        )
        self.assertEqual(test_case.name, "Example test")

    def test_test_case_requires_at_least_one_step(self):
        with self.assertRaises(ValidationError):
            TestCase(
                name="Empty test",
                description="Test without steps",
                steps=[]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
