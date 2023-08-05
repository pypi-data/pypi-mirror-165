from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess  # noqa: S404
from typing import Any, Optional

from pdf_information.encrypted import Encrypted
from pdf_information.mapping import convert_line_to_key_val


@dataclass
class PDFInfo:
    user_properties: bool
    suspects: bool
    page_rot: int
    pdf_version: str
    java_script: bool = False
    optimized: bool = False
    title: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None
    author: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    mod_date: Optional[str] = None
    custom_metadata: Optional[bool] = None
    metadata_stream: Optional[bool] = None
    tagged: Optional[bool] = None
    form: Optional[str] = None
    pages: Optional[int] = None
    encrypted: Optional[Encrypted] = None
    page_size: Optional[str] = None
    file_size: Optional[str] = None

    @classmethod
    def from_cmd_output(cls, cmd_output: bytes) -> PDFInfo:
        cls_dict: dict[str, Any] = {}
        for key, val in map(convert_line_to_key_val, cmd_output.splitlines()):
            cls_dict[key] = val
        return cls(**cls_dict)

    @classmethod
    def from_cmd(cls, pdf_file: Path) -> PDFInfo:
        cmd_output: bytes = subprocess.check_output(["pdfinfo", pdf_file])  # noqa: S603,S607 TODO
        return cls.from_cmd_output(cmd_output=cmd_output)
