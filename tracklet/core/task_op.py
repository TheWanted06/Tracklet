# tracklet/task_op.py

from typing import Dict, Any, Tuple
from tracklet.data_access.file_io import load_task, save_task
from .rules_engine import evaluate_rules
from .actions import action_registry
from .validators import validate_task

def create_task(task_data: Dict[str, Any], context: Dict[str, Any]) -> Tuple[bool, list]:
    is_valid, errors = validate_task(task_data)
    if not is_valid:
        return False, errors

    save_task(task_data)
    context.update(task_data)
    evaluate_rules("on_task_created", context, action_registry)
    return True, []

def update_task(task_data: Dict[str, Any], context: Dict[str, Any]) -> Tuple[bool, list]:
    is_valid, errors = validate_task(task_data)
    if not is_valid:
        return False, errors

    save_task(task_data)
    context.update(task_data)
    evaluate_rules("on_task_updated", context, action_registry)
    return True, []

def submit_task(task_id: str, context: Dict[str, Any]) -> Tuple[bool, list]:
    task = load_task(task_id)
    if not task:
        return False, ["Task not found"]

    context.update(task)
    evaluate_rules("on_submission", context, action_registry)
    return True, []
