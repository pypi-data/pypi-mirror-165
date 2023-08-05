from typing import Any, Callable, Optional

from pdf_information.encrypted import Encrypted
from pdf_information.snake_case import convert_to_snake_case
from pdf_information.value_conversion import value_conversion


def convert_line_to_key_val(line: bytes) -> tuple[str, Any]:
    key_val_split = line.decode().split(":", maxsplit=1)
    key = convert_to_snake_case(convert=key_val_split[0])
    str_value = key_val_split[1].strip()
    return key, parse_value(key=key, raw_value=str_value)


conversion: dict[str, Callable] = {
    "encrypted": Encrypted.from_cmd_output_line,
    "pages": int,
    "page_rot": int,
}


def encrypted(raw_value: str) -> Optional[Encrypted]:
    if raw_value == "no":
        return None
    return Encrypted.from_cmd_output_line(line=raw_value)


def parse_value(key: str, raw_value: str) -> Any:
    return conversion.get(key, value_conversion)(raw_value)
