def soft_assert_equal(actual, expected, message: str, errors: list[str]) -> None:
    if actual != expected:
        errors.append(f"{message} Actual: '{actual}', expected: '{expected}'")


def soft_assert_dict(actual: dict, expected: dict):
    errors = []

    for key, expected_value in expected.items():
        actual_value = actual.get(key)

        if actual_value != expected_value:
            errors.append(
                f"[{key}] expected={expected_value}, actual={actual_value}"
            )

    if errors:
        raise AssertionError(
            "Soft assertion failed:\n" + "\n".join(errors)
        )
