import os
from InquirerPy import inquirer
from .tracker import collect_all_tags

def prompt_tags_with_autocomplete(base_path, action=None,default_tags=None):
    existing_tags = collect_all_tags(base_path)
    default_tags = default_tags or []

    if not existing_tags:
        # Fallback to simple input if no tags exist
        tags_input = input("Enter tags (comma-separated): ").strip()
        return [t.strip() for t in tags_input.split(",") if t.strip()]
    try:
        if action is not None: 
                new_message="Tags (autocomplete, select multiple with space):",
        else: 
            new_message=f"Enter tags to {action} (comma-separated):",
        selected_tags = inquirer.fuzzy(
            message = new_message,
            choices=existing_tags,
            multiselect=True,
            default=default_tags,
            instruction="Type to autocomplete, space to select, enter to confirm",
        ).execute()
        return selected_tags
    except KeyboardInterrupt:
        return default_tags

def is_project_folder(path):
    return os.path.isfile(os.path.join(path, ".projectmeta"))
