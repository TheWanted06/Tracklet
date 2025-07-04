# Tracklet

Tracklet is a lightweight, local project tracking and metadata management tool designed for developers who want to organize, tag, and monitor progress of their projects easily on Windows and WSL environments.

## 🚀 Features

- Project initialization with metadata (`.projectmeta`)
- Task and Deliverable CRUD support via CLI
- YAML-driven rule engine for automated workflows
- Dynamic CLI prompts (powered by `InquirerPy`)
- Git integration (tagging, pushing)
- Changelog tracking
- Tag autocomplete and validation
- Modular and testable architecture

## 🗂️ Project Structure

Tracklet/
├── tracklet/
│ ├── cli/ # CLI entrypoints
│ ├── core/ # Business logic and rule engine
│ ├── data_access/ # YAML file I/O and project tracking
│ ├── utils/ # Prompting and formatting helpers
├── rules/ # YAML definitions for metadata, validation, rules
├── scripts/ # Project scripts (init, update, etc.)

## Installation

1. Clone or download the repository.
2. Install dependencies and the package globally (or in your virtual environment):

```bash
pip install --editable .
```

This installs all required dependencies automatically, including `InquirerPy`, `PyYAML`, and `Rich`.

3. Ensure your Python user scripts directory (e.g., `~/.local/bin` or `%APPDATA%\Python\Scripts`) is in your system `PATH` so you can run `tracklet` from the command line.

## Usage

tracklet project init
tracklet task create
tracklet deliverable list

### Command Overview

| Command  | Description                                             | Context                |
|----------|---------------------------------------------------------|------------------------|
| `init`   | Initialize current directory as a Tracklet project      | Must run inside project |
| `uninit` | Remove Tracklet metadata from current project           | Must run inside project |
| `update` | Update project metadata and progress                     | Project dir or main dir |
| `list`   | List projects and folders in a directory                 | Main projects directory |
| `search` | Search projects by metadata filters                      | Main projects directory |

---

### Detailed Command and Examples

#### Initialize a project (defaults to current directory and directory name as project name)

```bash
tracklet init --name "My Project"
```

#### or simply

```bash
tracklet init
```

- Prompts for all metadata interactively.
- Prevents duplicate initialization (warns if already initialized).
- Use --force to overwrite existing metadata if needed.

#### Update project metadata and progress

Update any combination of project properties:

```bash
tracklet update --stage "Development"  --tag -a "backend,api" --author "Alice"
```

- Supports adding, removing, or replacing tags:  
  - Replace tags: `--tag "tag1,tag2"`  
  - Add tags: `--tag -a "tag3"`  
  - Remove tags: `--tag -r "tag1"`  
- Interactive prompts with autocomplete appear if flags are used without values.
- Works inside project directories or from main directory with project selection prompt.

---

#### Search projects by tag, stage, author, or description

```bash
tracklet search --tag react-native
tracklet search --stage "Development"
tracklet search --author "Alice"
```

- Supports include and exclude filters.
- Interactive filter builder if no flags are provided.
- Displays results in a rich, color-coded table.

---

#### List all projects and folders in a directory

```bash
tracklet list
```

#### or specify a directory

```bash
tracklet list /path/to/projects
```

- Lists immediate subfolders.
- Indicates which folders are initialized projects.
- Shows tags, stages, and other metadata in detailed mode (`--detailed`).

---

#### Uninitialize a project

Remove Tracklet metadata from the current project directory:

```bash
tracklet uninit
```

- Prompts for confirmation unless `--force` is used.

## 🧩 Extending

-Add rules to rules/operations/ for automated actions
-Modify metadata in .projectmeta
-Customize prompts in tracklet/utils/prompt.py

## Unistallation

To uninstall Tracklet from your environment, run:

```bash
pip uninstall tracklet
```

This removes the package and its CLI command from your system.

To remove build artifacts, caches, and metadata after unistalling, run:

```bach
python scripts/clean.py
```

This will remove `__pycache__`, `.egg-info`, build folders, and other common leftovers.

## Project Stages

Tracklet uses the following predefined stages for project progress tracking:

- Planning
- Development
- Staging
- Testing
- Production
- Abandoned
- On Hold

---

## Versioning

Tracklet’s version is stored in `tracklet/_version.py` and is updated for each release.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Pull requests and issues are welcome. Please ensure tests are updated accordingly.

---

## Troubleshooting

If `tracklet` is not found, ensure your scripts directory is in your PATH and reinstall with `pip install --user .` or `pip install --editable .`.

If you see ModuleNotFoundError: No module named 'InquirerPy', install the dependency manually:
 `pip install InquirerPy`.

---
