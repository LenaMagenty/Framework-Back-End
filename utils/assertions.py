def soft_assert_equal(actual, expected, message: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{message} Actual: '{actual}', expected: '{expected}'")