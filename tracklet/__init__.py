# tracklet/__init__.py

# Package initialization for project_tracker
# Expose core modules for easy imports

from .data_access.metadata import read_metadata, write_metadata, create_default_metadata
from .data_access.tracker import find_projects, filter_projects, summarize_progress
from tracklet.cli.cli import main as cli_main
from tracklet.utils.prompt import is_project_folder
from tracklet._version import __version__

__all__ = [
    "read_metadata",
    "write_metadata",
    "create_default_metadata",
    "find_projects",
    "filter_projects",
    "summarize_progress",
    "cli_main",
    "is_project_folder",
    "__verion__",
]
