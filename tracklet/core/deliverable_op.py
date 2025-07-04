
from typing import Dict, Any, Tuple
from tracklet.data_access.file_io import save_deliverable
from .rules_engine import evaluate_rules
from .actions import action_registry
from .validators import validate_deliverable

def create_deliverable(data: Dict[str, Any], context: Dict[str, Any]) -> Tuple[bool, list]:
    is_valid, errors = validate_deliverable(data)
    if not is_valid:
        return False, errors

    save_deliverable(data)
    context.update(data)
    evaluate_rules("on_deliverable_created", context, action_registry)
    return True, []

def update_deliverable(data: Dict[str, Any], context: Dict[str, Any]) -> Tuple[bool, list]:
    is_valid, errors = validate_deliverable(data)
    if not is_valid:
        return False, errors

    save_deliverable(data)
    context.update(data)
    evaluate_rules("on_deliverable_updated", context, action_registry)
    return True, []
