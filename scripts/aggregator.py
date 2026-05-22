from collections import defaultdict
from pathlib import Path
from typing import Any


def aggregate_students(raw_records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    students: dict[str, dict[str, Any]] = {}

    for record in raw_records:
        student_id = record.get("student_id") or record.get("student_name")
        if not student_id:
            continue

        key = str(student_id).strip()
        if key not in students:
            students[key] = {
                "student_id": record.get("student_id"),
                "student_name": record.get("student_name"),
                "class": record.get("class"),
                "history": [],
            }

        students[key]["history"].append(
            {
                "activity_name": record.get("activity_name"),
                "source_file": record.get("source_file"),
                "score": record.get("score"),
            }
        )

    return {"students": list(students.values())}
