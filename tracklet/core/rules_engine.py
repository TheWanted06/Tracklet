# tracklet/rules_engine.py

import yaml
from pathlib import Path
from typing import Any, Dict, List, Callable

RULES_DIR = Path("rules/operations")

class Rule:
    """
    Represents a single automation rule loaded from YAML.
    Each rule defines:
      - a trigger name (e.g. on_task_saved)
      - an optional condition (as an expression)
      - one or more actions to execute
    """
    def __init__(self, rule_data: Dict[str, Any]):
        self.id = rule_data.get("id", "unnamed-rule")
        self.trigger = rule_data.get("trigger")
        self.condition = rule_data.get("condition")
        self.actions = rule_data.get("actions", [])

    def is_triggered_by(self, trigger_name: str) -> bool:
        return self.trigger == trigger_name

    def evaluate_condition(self, context: Dict[str, Any]) -> bool:
        if not self.condition:
            return True  # No condition means always true

        try:
            # Safe condition evaluation
            return eval(self.condition, {}, context)
        except Exception as e:
            print(f"[RuleEngine] Condition error in rule '{self.id}': {e}")
            return False

    def execute_actions(self, context: Dict[str, Any], action_registry: Dict[str, Callable]) -> None:
        for action in self.actions:
            if isinstance(action, str):
                action_name, params = action, {}
            elif isinstance(action, dict):
                action_name, params = next(iter(action.items()))
            else:
                print(f"[RuleEngine] Invalid action format in rule '{self.id}'")
                continue

            action_fn = action_registry.get(action_name)
            if not action_fn:
                print(f"[RuleEngine] Action '{action_name}' not found.")
                continue

            try:
                action_fn(context=context, **params)
            except Exception as e:
                print(f"[RuleEngine] Action '{action_name}' failed: {e}")


def load_rules(trigger_name: str) -> List[Rule]:
    """
    Loads all rule YAML files and filters those matching the given trigger.
    """
    rules = []
    for file in RULES_DIR.glob("*.yaml"):
        with open(file, "r") as f:
            try:
                rule_data = yaml.safe_load(f)
                if isinstance(rule_data, list):
                    for entry in rule_data:
                        rule = Rule(entry)
                        if rule.is_triggered_by(trigger_name):
                            rules.append(rule)
            except Exception as e:
                print(f"[RuleEngine] Failed to parse {file}: {e}")
    return rules


def evaluate_rules(trigger: str, context: Dict[str, Any], action_registry: Dict[str, Callable]) -> None:
    """
    Main evaluation entrypoint.
    Loads and executes rules based on trigger name and context.
    """
    print(f"[RuleEngine] Evaluating rules for trigger: '{trigger}'")
    for rule in load_rules(trigger):
        if rule.evaluate_condition(context):
            print(f"[RuleEngine] ✅ Rule matched: {rule.id}")
            rule.execute_actions(context, action_registry)
        else:
            print(f"[RuleEngine] ❌ Rule skipped: {rule.id} (condition false)")


# --- Validation helpers (can be moved out to validators.py later) ---

def validate_task(task: Dict[str, Any]) -> (bool, List[str]):
    errors = []
    if not task.get("title"):
        errors.append("Task must have a title.")
    if task.get("priority") not in ["low", "medium", "high"]:
        errors.append("Invalid priority.")
    if task.get("status") not in ["todo", "in_progress", "blocked", "completed"]:
        errors.append("Invalid status.")
    return (len(errors) == 0), errors


def validate_deliverable(deliverable: Dict[str, Any]) -> (bool, List[str]):
    errors = []
    if not deliverable.get("title"):
        errors.append("Deliverable must have a title.")
    return (len(errors) == 0), errors
