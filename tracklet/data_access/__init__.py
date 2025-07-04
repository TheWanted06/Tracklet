# tracklet/data_access/__init__.py

from .file_io import (
    load_yaml_file,
    save_yaml_file,
    get_tasks_file,
    load_tasks,
    load_task,
    save_task,
    save_tasks,
    generate_task_id,
    generate_deliverable_id,
    load_deliverable,
    load_deliverables,
    save_deliverable,
    save_deliverables,
    generate_deliverable_id
)
from .metadata import (
    read_metadata,
    write_metadata,
    create_default_metadata,
    delete_metadata,
    STAGES
)
from .tracker import (
    find_projects,
    list_projects,
    filter_projects,
    summarize_progress,
    collect_all_tags
)
