from typing import Any, Optional


def value_conversion(raw_value: Optional[str] = None) -> Any:
    if not raw_value:
        return None
    if raw_value == "no":
        return False
    if raw_value == "yes":
        return True
    return raw_value
