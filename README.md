# Tracklet

Tracklet is a lightweight, local project tracking and metadata management tool designed for developers who want to organize, tag, and monitor progress of their projects easily on Windows and WSL environments.

## Features

- Initialize projects with metadata including name, description, author, tags, and progress stage.
- Track project progress via completed and todo task lists with automatic percentage calculation.
- Filter and search projects by tags, stage, or author.
- Command-line interface accessible globally after installation.
- Supports multiple project stages including Planning, Development, Staging, Production, Abandoned, and On Hold.
- Default project path is the current directory for convenience.
- Optional project name defaults to current directory name if not specified.

## Installation

1. Clone or download the repository.
2. Install dependencies and the package globally:

```bash
pip install --editable .
```

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

## Project Stages

- 🚧 Planning
- 🛠 Development
- ✅ Staging
- 🚀 Production
- 🛑 Abandoned
- ⏸ On Hold

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Pull requests and issues are welcome. Please ensure tests are updated accordingly.

---

## Troubleshooting

If `tracklet` command is not found after installation, ensure your Python scripts directory is in your PATH and restart your terminal session.

---


