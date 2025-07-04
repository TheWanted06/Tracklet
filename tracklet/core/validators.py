from typing import Dict, Tuple, List

def validate_task(task: Dict) -> Tuple[bool, List[str]]:
    errors = []
    if not task.get("title"):
        errors.append("Task must have a title.")
    if task.get("priority") not in ["low", "medium", "high"]:
        errors.append("Invalid priority level.")
    if task.get("status") not in ["todo", "in_progress", "blocked", "completed"]:
        errors.append("Invalid status.")
    return (len(errors) == 0), errors

def validate_deliverable(deliverable: Dict) -> Tuple[bool, List[str]]:
    errors = []
    if not deliverable.get("title"):
        errors.append("Deliverable must have a title.")
    if not deliverable.get("type"):
        errors.append("Deliverable type is required.")
    return (len(errors) == 0), errors
