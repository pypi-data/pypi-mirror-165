from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from pdf_information.snake_case import convert_to_snake_case
from pdf_information.value_conversion import value_conversion


@dataclass
class Encrypted:
    print: bool
    copy: bool
    change: bool
    add_notes: bool
    algorithm: str

    @classmethod
    def from_cmd_output_line(cls, line: str) -> Optional[Encrypted]:
        if line == "no":
            return None
        cls_dict: dict[str, Any] = {}
        for attribute_pair in line[5:-1].split(" "):
            str_key, str_val = attribute_pair.split(":")
            key = convert_to_snake_case(convert=str_key)
            cls_dict[key] = value_conversion(raw_value=str_val)
        return cls(**cls_dict)
