# PDF Information

Maps output of `pdfinfo` to a dataclass.

## Usage

```py
from pathlib import Path
from  pdf_information import PDFInfo

pdf_file = Path("pdf_files/some_file.pdf")
pdf_info = PDFInfo.from_cmd(pdf_file=pdf_file)
```

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
