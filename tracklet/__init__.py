# tracklet/__init__.py

# Package initialization for project_tracker
# Expose core modules for easy imports

from .metadata import read_metadata, write_metadata, create_default_metadata
from .tracker import find_projects, filter_projects, summarize_progress
from .cli import main as cli_main
from .utils import is_project_folder

__all__ = [
    "read_metadata",
    "write_metadata",
    "create_default_metadata",
    "find_projects",
    "filter_projects",
    "summarize_progress",
    "cli_main",
    "is_project_folder",
]
