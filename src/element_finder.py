from playwright.sync_api import Page


def find_element(
    page: Page,
    strategy: str,
    value: str,
    role: str = None
):
    """
    Find a webpage element using an accessible locator strategy.

    Supported strategies:
    - role
    - label
    - placeholder
    - text
    - test_id
    - css
    """

    if strategy == "role":
        if not role:
            raise ValueError("Role is required for role strategy.")

        locator = page.get_by_role(
            role,
            name=value,
            exact=True
        )

    elif strategy == "label":
        locator = page.get_by_label(value, exact=True)

    elif strategy == "placeholder":
        locator = page.get_by_placeholder(value, exact=True)

    elif strategy == "text":
        locator = page.get_by_text(value, exact=True)

    elif strategy == "test_id":
        locator = page.get_by_test_id(value)

    elif strategy == "css":
        locator = page.locator(value)

    else:
        raise ValueError(
            f"Unsupported locator strategy: {strategy}"
        )

    count = locator.count()

    if count == 0:
        raise LookupError(
            f"No element found using {strategy}: {value}"
        )

    if count > 1:
        raise LookupError(
            f"Multiple elements found using {strategy}: {value}. "
            "Use a more specific locator."
        )

    return locator