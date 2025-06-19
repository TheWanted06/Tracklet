import os
from .metadata import read_metadata

def collect_all_tags(base_path):
    tags_set = set()

    # Check base_path itself
    if os.path.isfile(os.path.join(base_path, ".projectmeta")):
        meta = read_metadata(base_path)
        if meta and "tags" in meta:
            tags_set.update(meta["tags"])

    # Check immediate subdirectories
    try:
        entries = os.listdir(base_path)
    except FileNotFoundError:
        return []

    for entry in entries:
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            meta_path = os.path.join(full_path, ".projectmeta")
            if os.path.isfile(meta_path):
                meta = read_metadata(full_path)
                if meta and "tags" in meta:
                    tags_set.update(meta["tags"])

    return sorted(tags_set)

def find_projects(base_path):
    projects = []

    # Check base_path itself
    if os.path.isfile(os.path.join(base_path, ".projectmeta")):
        meta = read_metadata(base_path)
        if meta:
            projects.append((base_path, meta))

    # List immediate subdirectories only (one level deep)
    try:
        entries = os.listdir(base_path)
    except FileNotFoundError:
        return projects

    for entry in entries:
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            if os.path.isfile(os.path.join(full_path, ".projectmeta")):
                meta = read_metadata(full_path)
                if meta:
                    projects.append((full_path, meta))
    return projects

def list_projects(base_path):
    """List all immediate subdirectories, showing if initialized or not."""
    try:
        entries = os.listdir(base_path)
    except FileNotFoundError:
        return []

    project_list = []
    for entry in entries:
        full_path = os.path.join(base_path, entry)
        if os.path.isdir(full_path):
            meta_path = os.path.join(full_path, ".projectmeta")
            if os.path.isfile(meta_path):
                meta = read_metadata(full_path)
                project_list.append({
                    "name": meta.get("name", entry),
                    "path": full_path,
                    "initialized": True,
                    "tags": meta.get("tags", []),
                    "stage": meta.get("progress", {}).get("stage", "Unknown")
                })
            else:
                project_list.append({
                    "name": entry,
                    "path": full_path,
                    "initialized": False,
                    "tags": [],
                    "stage": None
                })
    return project_list

def filter_projects(projects, tag=None, stage=None, author=None):
    filtered = []
    for path, meta in projects:
        if tag and tag not in meta.get("tags", []):
            continue
        if stage and stage != meta.get("progress", {}).get("stage"):
            continue
        if author and author != meta.get("author"):
            continue
        filtered.append((path, meta))
    return filtered

def summarize_progress(meta):
    tasks = meta.get("progress", {}).get("tasks", {})
    completed = len(tasks.get("completed", []))
    total = completed + len(tasks.get("todo", []))
    percent = (completed / total * 100) if total > 0 else 0
    return f"{percent:.1f}% ({completed}/{total} tasks)"
