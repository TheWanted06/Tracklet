# tracklet/actions.py

import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from .changelog import append_to_changelog


# --- Git-related Actions ---

def create_git_tag(context: Dict[str, Any], tag: str) -> None:
    """Creates a Git tag for version tracking."""
    try:
        subprocess.run(["git", "tag", tag], check=True)
        print(f"🏷️ Git tag '{tag}' created.")
    except subprocess.CalledProcessError:
        print("❌ Failed to create git tag.")


def push_git_tags(context: Dict[str, Any]) -> None:
    """Pushes all local Git tags to remote."""
    try:
        subprocess.run(["git", "push", "--tags"], check=True)
        print("🚀 Git tags pushed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to push git tags.")


# --- Notification and Logging ---

def notify_user(context: Dict[str, Any], message: str = "Task notification") -> None:
    """Prints a user notification message."""
    print(f"🔔 Notify: {message} | Context: {context.get('task_id', 'N/A')}")


def validate_file_schema(context: Dict[str, Any], file: str) -> None:
    """Validates file schema (placeholder for future validation engine)."""
    print(f"✅ Schema validation for {file} (placeholder — implement real validation)")


# --- File Manipulation ---

def remove_task_from_file(
    context: Dict[str, Any], file: str, task_id_field: str = "id"
    ) -> None:
    """Removes a task with matching task_id from a YAML file."""
    path = Path(file)
    if not path.exists():
        print(f"⚠️ File {file} not found.")
        return

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data.get("tasks"), list):
        print(f"❌ No tasks found in {file}")
        return

    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t.get(task_id_field) != context.get("task_id")]
    after = len(data["tasks"])

    if before == after:
        print(f"ℹ️ Task {context.get('task_id')} not found in {file}")
    else:
        with open(path, "w") as f:
            yaml.dump(data, f)
        print(f"🗑️ Removed task {context.get('task_id')} from {file}")


# --- Action Registry (used by rule engine) ---

action_registry: Dict[str, Any] = {
    "notify": notify_user,
    "git_tag": create_git_tag,
    "push_tags": push_git_tags,
    "remove_from": remove_task_from_file,
    "append_changelog": append_to_changelog,
    "validate": validate_file_schema,
}
