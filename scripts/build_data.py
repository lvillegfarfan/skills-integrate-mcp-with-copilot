import argparse
import json
from pathlib import Path

from extractor import extract_links
from downloader import download_documents
from parser import parse_documents
from aggregator import aggregate_students


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build student data from an Excel spreadsheet of document links"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the Excel workbook containing document links",
    )
    parser.add_argument(
        "--output",
        default="data",
        help="Directory where data files and logs will be written",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting links from {input_path}")
    links = extract_links(str(input_path))
    print(f"Found {len(links)} document links")

    download_dir = output_dir / "downloads"
    error_log = output_dir / "error_links.json"
    downloaded_files, errors = download_documents(
        links, download_dir=str(download_dir), error_log_path=str(error_log)
    )

    print(f"Downloaded {len(downloaded_files)} documents")
    if errors:
        print(f"Logged {len(errors)} failed downloads to {error_log}")

    raw_activities = parse_documents(downloaded_files)
    raw_path = output_dir / "raw_activities.json"
    write_json(raw_path, raw_activities)
    print(f"Wrote raw activity records to {raw_path}")

    students = aggregate_students(raw_activities)
    students_path = output_dir / "students.json"
    write_json(students_path, students)
    print(f"Wrote aggregated students to {students_path}")


if __name__ == "__main__":
    main()
