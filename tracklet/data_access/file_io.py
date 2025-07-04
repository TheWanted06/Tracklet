
import yaml
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_yaml_file(file_path: Path) -> Optional[Dict]:
    if not file_path.exists():
        return None
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def save_yaml_file(file_path: Path, data: Dict):
    with open(file_path, "w") as f:
        yaml.dump(data, f)

# --- Task I/O ---
def get_tasks_file(file_path: Path) -> Path:
    return file_path / "tasks.yaml"

def load_tasks(file: str = "tasks.yaml") -> List[Dict[str, Any]]:
    path = Path(file)
    if path.exists():
        with open(path, "r") as f:
            return yaml.safe_load(f).get("tasks", [])
    return []

def save_tasks(tasks: List[Dict[str, Any]], file: str = "tasks.yaml"):
    with open(file, "w") as f:
        yaml.dump({"tasks": tasks}, f)

def load_task(task_id: str, file: str = "tasks.yaml") -> Dict[str, Any]:
    return next((t for t in load_tasks(file) if t.get("id") == task_id), {})

def save_task(task: Dict[str, Any], file: str = "tasks.yaml"):
    tasks = [t for t in load_tasks(file) if t.get("id") != task["id"]]
    tasks.append(task)
    save_tasks(tasks, file)

def generate_task_id() -> str:
    return str(uuid.uuid4())

# --- Deliverable I/O ---
def get_deliverables_file(project_path: Path) -> Path:
    return project_path / "deliverables.yaml"

def load_deliverables(file: str = "deliverables.yaml") -> List[Dict[str, Any]]:
    path = Path(file)
    if path.exists():
        with open(path, "r") as f:
            return yaml.safe_load(f).get("deliverables", [])
    return []

def save_deliverables(deliverables: List[Dict[str, Any]], file: str = "deliverables.yaml"):
    with open(file, "w") as f:
        yaml.dump({"deliverables": deliverables}, f)

def load_deliverable(deliverable_id: str, file: str = "deliverables.yaml") -> Dict[str, Any]:
    return next((d for d in load_deliverables(file) if d.get("id") == deliverable_id), {})

def save_deliverable(deliverable: Dict[str, Any], file: str = "deliverables.yaml"):
    deliverables = [d for d in load_deliverables(file) if d.get("id") != deliverable["id"]]
    deliverables.append(deliverable)
    save_deliverables(deliverables, file)

def generate_deliverable_id() -> str:
    return str(uuid.uuid4())