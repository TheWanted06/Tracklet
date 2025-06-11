import yaml
import os
from datetime import datetime

META_FILENAME = ".projectmeta"

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
            "milestones": []
        },
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    write_metadata(project_path, data)
