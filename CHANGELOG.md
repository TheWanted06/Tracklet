# Changelog

All notable changes to Tracklet are documented here to provide a clear and detailed history of the project’s development.

---

## [v0.5.0] - 2025-06-27

### 🧱 Major Refactor

- Completely modularized CLI into:
  - `project_cli.py`
  - `task_cli.py`
  - `deliverable_cli.py`
- Separated business logic into `core/`:
  - `task_ops.py`, `deliverable_ops.py`, `rules_engine.py`, etc.
- Created `data_access/`:
  - `file_io.py`, `metadata.py`, `tracker.py`
- Implemented autocomplete tag selection using `InquirerPy.fuzzy()`
- Added fallback for empty autocomplete to prevent crashes
- Introduced `utils/formats.py` with rich console formatting
- Added tag collection from existing `.projectmeta` files
- Added validation to tasks and deliverables
- Ensured `setup.py` uses proper `entry_points` and installable CLI
- Fixed all import issues post-refactor
- Fully functional `tracklet project init` with prompts

### 🐛 Fixes

- CLI now correctly handles invalid commands and missing metadata
- Improved feedback for missing or invalid project folders

---

## [0.4.0] - 2025-06-21

### Added

- Support for short flags alongside long flags for all commands and properties (e.g., `--tag` / `-t`, `--stage` / `-s`, `--author` / `-a`), improving CLI usability and efficiency.
- Tag update operations enhanced to support three modes: replace (`--tag`), add (`--tag -a`), and remove (`--tag -r`), with interactive fuzzy autocomplete prompts when values are omitted.
- Centralized reusable function `prompt_tags_with_autocomplete` introduced to provide consistent and user-friendly tag input across all commands.
- Integration of the Rich library to display color-coded, well-formatted terminal tables in `list` and `search` commands, enhancing readability and user experience.
- Interactive filter builder added to the `search` command, supporting include/exclude filters and multi-value inputs for flexible project querying.
- Context-aware command execution enforced:
  - `init` and `uninit` commands restricted to run only inside project directories.
  - `list` and `search` commands restricted to the main projects directory.
  - `update` command allowed in both contexts, with project selection prompt when run from the main directory.
- Confirmation prompts implemented before any destructive actions (e.g., uninitializing projects) and before saving metadata updates to prevent accidental changes.

### Changed

- Refactored CLI handler structure for improved modularity, allowing reuse of autocomplete prompts and better maintainability.
- Enhanced filtering logic with case-insensitive substring matching, making searches more flexible and user-friendly.
- Improved user experience by adding interactive prompts when flags are provided without values, reducing errors and confusion.
- Unified CLI flag parsing and sub-flag handling for tag operations (add/remove), streamlining command syntax.
- Updated display formatting in terminal outputs for better clarity and visual appeal.

### Fixed

- Corrected bugs related to tag updating modes that caused incorrect metadata overwriting.
- Fixed command context detection to prevent commands from running in inappropriate directories.
- Resolved edge cases in interactive prompts and fixed display inconsistencies in search and list outputs.

### Removed

- Removed emoji icons from project stage labels to ensure consistent CLI compatibility across platforms and terminals.

---

## [0.3.0] - 2025-06-19

### Added

- Interactive stage selection prompts implemented during project initialization and updates, improving user input accuracy.
- New `uninit` command added to safely remove Tracklet metadata from projects.
- Duplicate initialization prevention added to `init` command, with clear user feedback to avoid accidental overwrites.
- Single-source versioning system introduced, centralizing version information and providing guidance for version updates.
- Documentation expanded to include automatic dependency installation instructions and cleanup procedures.

---

## [0.2.5] - 2025-06-12

### Added

- New `list` command implemented to display all folders within a directory, marking which are initialized Tracklet projects and showing their tags and stages.
- Enhanced `init` command to prompt interactively for all project metadata fields, including selection of project stage from a predefined list.
- Improved CLI argument handling to default to the current directory when no path is specified, simplifying command usage.
- README updated with detailed instructions for uninstalling Tracklet and usage examples for the new `list` command.

### Fixed

- Corrected syntax errors affecting the `search` command.
- Improved search functionality to work correctly in directories without Tracklet initialization.
- Modified search to limit directory traversal to the current directory and its immediate subfolders, improving performance and relevance.

---

## [0.2.0] - 2025-06-12

### Added

- Core CLI commands introduced: `init`, `update`, and `search`, all supporting default operation in the current directory.
- Flexible project metadata structure added, including fields for name, description, author, tags, stage, and task lists.
- Progress tracking implemented as a percentage based on completed and todo tasks.
- Multiple project stages defined, including special statuses like Abandoned and On Hold.
- Package configured for global CLI access via `setup.py` entry point for easy installation and usage.
- Initial README created, covering installation, usage, and troubleshooting.
- MIT license added for permissive open source distribution.

---

## [0.1.0] - 2025-06-11

### Added

- Core Python modules developed:
  - `metadata.py` for reading and writing `.projectmeta` YAML metadata files.
  - `tracker.py` handling project discovery, filtering, and progress summarization.
  - `cli.py` providing command-line interface for `init`, `update`, and `search`.
  - `utils.py` containing helper functions for project folder detection.
- Bash scripts created for common operations:
  - `init_project.sh` for interactive project initialization.
  - `update_project.sh` for updating metadata fields.
  - `search_projects.sh` for searching and filtering projects by tags, stage, or author.
- `__init__.py` added to expose core functions for easy imports.
- Established foundation for a cross-platform, local project tracking and tagging system optimized for Windows and WSL environments.

---
