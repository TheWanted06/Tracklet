import os
from .metadata import read_metadata

def find_projects(base_path):
    projects = []
    for root, dirs, files in os.walk(base_path):
        if ".projectmeta" in files:
            meta = read_metadata(root)
            if meta:
                projects.append((root, meta))
    return projects

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
