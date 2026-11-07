
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator
)


class TestAction(BaseModel):

    action: Literal[
        "navigate",
        "click",
        "fill",
        "assert_text",
        "assert_title",
        "wait"
    ]

    url: str | None = None
    strategy: Literal[
        "role",
        "label",
        "placeholder",
        "text",
        "test_id",
        "css"
    ] | None = None

    value: str | None = None
    role: str | None = None
    text: str | None = None

    timeout_ms: int = 5000

    @field_validator("timeout_ms", mode="before")
    @classmethod
    def set_default_timeout(cls, value):
        if value is None or value == 0 or value == "0":
            return 5000
        return value

    @model_validator(mode="after")
    def validate_action(self):

        if not 1 <= self.timeout_ms <= 60000:
            raise ValueError(
                "timeout_ms must be between 1 and 60000."
            )

        if self.action == "navigate":
            if not self.url:
                raise ValueError(
                    "Navigate action requires a URL."
                )

            if not self.url.startswith(("http://", "https://")):
                raise ValueError(
                    "URL must start with http:// or https://"
                )

        if self.action in ["click", "fill"]:
            if not self.strategy:
                raise ValueError(
                    f"{self.action} requires a locator strategy."
                )

            if not self.value:
                raise ValueError(
                    f"{self.action} requires a locator value."
                )

        if self.strategy == "role" and not self.role:
            raise ValueError("Role strategy requires a role.")

        if self.action == "fill" and self.text is None:
            raise ValueError("Fill action requires text.")

        if self.action in ["assert_text", "assert_title"]:
            if self.text is None:
                raise ValueError(
                    f"{self.action} requires expected text."
                )

        return self


class TestCase(BaseModel):

    name: str
    description: str

    steps: list[TestAction] = Field(min_length=1)
