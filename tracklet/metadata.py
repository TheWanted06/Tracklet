import yaml
import os
from datetime import datetime

META_FILENAME = ".projectmeta"

STAGES = [
    "Planning",
    "Development",
    "Staging",
    "Testing",
    "Launched",
    "Abandoned",
    "On Hold"
]

def read_metadata(project_path):
    meta_path = os.path.join(project_path, META_FILENAME)
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, "r") as f:
        return yaml.safe_load(f)

def write_metadata(project_path, data):
    meta_path = os.path.join(project_path, META_FILENAME)
    data['last_updated'] = datetime.now().strftime("%Y-%m-%d")
    with open(meta_path, "w") as f:
        yaml.dump(data, f)

def create_default_metadata(project_path, name, description, author, tags, stage):
    data = {
        "name": name,
        "description": description,
        "author": author,
        "tags": tags,
        "progress": {
            "stage": stage,
            "tasks": {
                "completed": [],
                "todo": []
            }
        },
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    write_metadata(project_path, data)

def delete_metadata(project_path):
    """Delete the .projectmeta file if it exists."""
    meta_path = os.path.join(project_path, META_FILENAME)
    if os.path.isfile(meta_path):
        os.remove(meta_path)
        return True
    return False
