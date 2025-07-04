# tracklet/changelog.py

import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

def load_changelog(file: str = "changelog.yaml") -> List[Dict[str, Any]]:
    """
    Loads changelog entries from a YAML file.
    Returns an empty list if file does not exist or is empty.
    """
    path = Path(file)
    if path.exists():
        with open(path, "r") as f:
            return yaml.safe_load(f) or []
    return []


def save_changelog(entries: List[Dict[str, Any]], file: str = "changelog.yaml") -> None:
    """
    Saves a list of changelog entries to the given YAML file.
    """
    with open(Path(file), "w") as f:
        yaml.dump(entries, f)


def append_to_changelog(context: Dict[str, Any], file: str = "changelog.yaml") -> None:
    """
    Appends a new changelog entry using task context.
    """
    entries = load_changelog(file)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "task_id": context.get("task_id"),
        "summary": context.get("summary", "No summary provided"),
        "author": context.get("author"),
        "status": context.get("status"),
        "stage": context.get("stage"),
    }

    entries.append(entry)
    save_changelog(entries, file)
    print(f"📝 Changelog updated for task {context.get('task_id')}")
