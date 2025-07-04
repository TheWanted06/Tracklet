from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from typing import List
from pathlib import Path
import yaml
import os

from tracklet.data_access.tracker import collect_all_tags

def prompt_text(message: str, default: str = "") -> str:
    """Prompt a single line of text."""
    return inquirer.text(message=message, default=default).execute()

def prompt_text_list(message):
    """Prompt for comma-separated list and return list of trimmed strings."""
    text = inquirer.text(message=message).execute()
    return [t.strip() for t in text.split(",") if t.strip()]

def prompt_select(message: str, choices: List[str], default: str = None) -> str:
    """Prompt a single-select choice list."""
    return inquirer.select(
        message=message,
        choices=choices,
        default=default,
        cycle=True
    ).execute()


def prompt_multi_select(message: str, choices: List[str], default: List[str] = []) -> List[str]:
    """Prompt a multi-select checkbox list."""
    return inquirer.checkbox(
        message=message,
        choices=[Choice(name=ch, enabled=ch in default) for ch in choices],
        cycle=True,
    ).execute()


def prompt_tags_with_autocomplete(project_path: str = ".", mode: str = "Add") -> List[str]:
    """Prompt user for tags with autocomplete suggestions."""
    # Try to gather all tags from existing metadata or tag_schema
    try:
        choices = collect_all_tags(project_path)
        if choices is null:
            choices=_load_all_tags(project_path)
        choices = sorted(set(choices))  # Clean + deduplicate
    except Exception:
        choices = []

    if not choices:
        # Fallback plain input if no tags
        print("⚠️ No existing tags found. Please enter tags manually (comma-separated):")
        tag_input = input("Tags: ").strip()
        return [tag.strip() for tag in tag_input.split(",") if tag.strip()]

    # Normal fuzzy prompt
    selected_tags = inquirer.fuzzy(
        message="Select or type tags:",
        choices=choices,
        multiselect=True,
        validate=lambda result: len(result) > 0,
        instruction="Use arrow keys or type to search (press space to select, enter to confirm)",
    ).execute()
    return selected_tags
    #tag_choices = _load_all_tags(project_path)
    
    inquirer.fuzzy(
        message=f"{mode} Tags (type to filter):",
        choices=tag_choices,
        multiselect=True,
        validate=lambda result: isinstance(result, list),
        instruction="Use arrows and spacebar to select. Enter to confirm.",
    ).execute()


def _load_all_tags(project_path: str) -> List[str]:
    """Internal helper to collect all tags from rules/tag_schema.yaml."""
    schema_path = Path("rules/definitions/tag_schema.yaml")
    if schema_path.exists():
        with open(schema_path, "r") as f:
            try:
                tag_schema = yaml.safe_load(f)
                if isinstance(tag_schema, dict):
                    return list(tag_schema.get("tags", []))
                elif isinstance(tag_schema, list):
                    return tag_schema
            except Exception:
                pass
    return []

def is_project_folder(path):
    return os.path.isfile(os.path.join(path, ".projectmeta"))
