from pathlib import Path
import re

URL_PATTERN = re.compile(r"(https?://\S+|file://\S+)", re.IGNORECASE)
VALID_EXTENSIONS = {".docx", ".xlsx"}


def normalize_url(value: str) -> str | None:
    if not value:
        return None
    text = value.strip()
    if text.startswith("file://"):
        return text

    match = URL_PATTERN.search(text)
    if not match:
        return None

    url = match.group(1).strip().rstrip(".,;\n\r")
    if url.startswith("file://"):
        return url

    if Path(url).suffix.lower() in VALID_EXTENSIONS:
        return url

    return url if url.lower().startswith("http") else None


def extract_links(excel_path: str) -> list[dict[str, str]]:
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError("openpyxl is required to extract links from Excel files") from exc

    workbook = openpyxl.load_workbook(excel_path, data_only=True)
    links: list[dict[str, str]] = []

    for sheet in workbook.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell is None or cell.value is None:
                    continue

                candidate = None
                if getattr(cell, "hyperlink", None):
                    candidate = cell.hyperlink.target
                elif isinstance(cell.value, str):
                    candidate = cell.value

                url = normalize_url(str(candidate)) if candidate else None
                if not url:
                    continue

                ext = Path(url.replace("file://", "")).suffix.lower()
                if ext not in VALID_EXTENSIONS:
                    continue

                links.append({
                    "source": f"{sheet.title}:{cell.coordinate}",
                    "url": url,
                })

    return links
