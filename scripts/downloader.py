import json
import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests


def _local_path(url: str) -> Path | None:
    if url.startswith("file://"):
        return Path(url[len("file://") :])
    candidate = Path(url)
    return candidate if candidate.exists() else None


def download_documents(
    links: list[dict[str, str]],
    download_dir: str,
    error_log_path: str | None = None,
) -> tuple[list[str], list[dict[str, str]]]:
    download_path = Path(download_dir)
    download_path.mkdir(parents=True, exist_ok=True)

    downloaded_files: list[str] = []
    errors: list[dict[str, str]] = []

    for index, link in enumerate(links, start=1):
        url = link["url"]
        parsed = urlparse(url)
        name = Path(parsed.path).name or f"document_{index}"
        target = download_path / name

        local_source = _local_path(url)
        if local_source is not None:
            try:
                shutil.copy(local_source, target)
                downloaded_files.append(str(target))
                continue
            except Exception as exc:
                errors.append({"source": link["source"], "url": url, "error": str(exc)})
                continue

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            target.write_bytes(response.content)
            downloaded_files.append(str(target))
        except Exception as exc:
            errors.append({"source": link["source"], "url": url, "error": str(exc)})

    if error_log_path:
        Path(error_log_path).parent.mkdir(parents=True, exist_ok=True)
        Path(error_log_path).write_text(json.dumps(errors, indent=2), encoding="utf-8")

    return downloaded_files, errors
