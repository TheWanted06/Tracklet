# Tracklet

Tracklet is a lightweight, local project tracking and metadata management tool designed for developers who want to organize, tag, and monitor progress of their projects easily on Windows and WSL environments.

## Features

- Initialize projects with metadata (name, description, author, tags, stage).
- Interactive prompts for project stage (with arrow-key selection) and tag autocomplete.
- Update project metadata and progress interactively.
- Search and filter projects by tag, stage, or author (with tag autocomplete).
- List all projects and folders in a directory, showing which are initialized.
- Uninit a project to remove its metadata.
- Prevents duplicate initialization and warns if a project is already initialized.
- Easy version management with a single-source version string.
- Automatic dependency installation via setup.py.

## Installation

1. Clone or download the repository.
2. Install dependencies and the package globally:

```bash
pip install --editable .
```

All required dependencies (e.g. InquirerPy, PyYAML) are installed automatically.

3. Ensure your Python user scripts directory (e.g., `~/.local/bin`) is in your PATH.

## Usage

### Initialize a project (defaults to current directory and directory name as project name)

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

### Update project metadata and progress

```bash
tracklet update --stage "🛠 Development" --completed "Setup,Core Features" 
--todo "Testing,Documentation"
```

### Search projects by tag or stage

```bash
tracklet search --tag react-native
tracklet search --stage "🛠 Development"
```

### List all projects and folders in a directory

```bash
tracklet list
```

#### or specify a directory

```bash
tracklet list /path/to/projects
```

this command lists all immediate subfolders, indication which are initialized with Tracklet, along with their tags and stages

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

- 🚧 Planning
- 🛠 Development
- ✅ Staging
- 🚀 Production
- 🛑 Abandoned
- ⏸ On Hold

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

If you see ModuleNotFoundError: No module named 'InquirerPy', run `pip install InquirerPy`.

---
