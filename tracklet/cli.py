import argparse
import os
from pathlib import Path
from .metadata import create_default_metadata, read_metadata, write_metadata, STAGES
from .tracker import find_projects, filter_projects, summarize_progress, list_projects, collect_all_tags
from InquirerPy import inquirer

def prompt_stage(default="🚧 Planning"):
    stages = STAGES
    try:
        selected = inquirer.select(
            message="Select project stage:",
            choices=stages,
            default=default,
            cycle=True,
        ).execute()
        return selected
    except KeyboardInterrupt:
        return default

def prompt_tags_with_autocomplete(base_path, default_tags=None):
    existing_tags = collect_all_tags(base_path)
    if not existing_tags:
        return input("Enter tags (comma-separated): ").split(",")
    default_tags = default_tags or []

    try:
        selected_tags = inquirer.fuzzy(
            message="Tags (autocomplete, select multiple with space):",
            choices=existing_tags,
            multiselect=True,
            default=default_tags,
            instruction="Type to autocomplete, space to select, enter to confirm",
        ).execute()
        return selected_tags
    except KeyboardInterrupt:
        return default_tags

def init_project(args):

    # Use provided path or default to current directory
    project_path = args.path

    # Check if project is already initialized
    meta_path = os.path.join(project_path, ".projectmeta")
    if os.path.exists(meta_path):
        print(f"Project at '{project_path}' is already initialized.")
        print("If you want to re-initialize, please uninit the project first or delete the existing .projectmeta file. Or else please use --force to overwrite existing metadata.")
        return

    # Default project name is the folder name
    default_name = os.path.basename(os.path.abspath(project_path))

    # Prompt for project name, showing default and allowing accept by Enter
    name = args.name
    if not name:
        prompt = f"Project name [{default_name}]: "
        name_input = input(prompt).strip()
        name = name_input if name_input else default_name

    # Prompt for description if not provided
    description = args.description
    if not description:
        description = input("Description (optional): ").strip()

    # Prompt for author if not provided
    author = args.author
    if not author:
        author = input("Author (optional): ").strip()

   # Prompt for tags with autocomplete
    tags = args.tags
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    else:
        tag_list = prompt_tags_with_autocomplete(project_path)

    # Prompt for stage with default
    stage = args.stage
    if not stage:
        stage = prompt_stage()
    elif stage not in STAGES:
        print(f"Warning: Stage '{stage}' not in predefined stages. Using as is.")

    # Validate project path exists
    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist.")
        return

    create_default_metadata(project_path, name, description, author, tag_list, stage)
    print(f"Initialized project metadata at {project_path}")

def uninit_project(args):
    project_path = args.path
    meta_path = os.path.join(project_path, ".projectmeta")
    if os.path.exists(meta_path):
        os.remove(meta_path)
        print(f"Removed .projectmeta from {project_path}. Project is now uninitialized.")
    else:
        print(f"No .projectmeta found in {project_path}. Project was not initialized.")

def update_project(args):
    project_path = args.path
    meta = read_metadata(project_path)
    if not meta:
        print("No metadata found to update.")
        return

    if args.name:
        meta['name'] = args.name
    if args.description:
        meta['description'] = args.description
    if args.author:
        meta['author'] = args.author
    if args.tags:
        meta['tags'] = [t.strip() for t in args.tags.split(",")]
    if args.stage:
        if args.stage not in STAGES:
            print(f"Warning: Stage '{args.stage}' not in predefined stages. Using as is.")
        meta['progress']['stage'] = args.stage

    # Update tasks if provided
    if args.completed or args.todo:
        if 'progress' not in meta:
            meta['progress'] = {}
        if 'tasks' not in meta['progress']:
            meta['progress']['tasks'] = {'completed': [], 'todo': []}
        if args.completed:
            meta['progress']['tasks']['completed'] = [t.strip() for t in args.completed.split(",")]
        if args.todo:
            meta['progress']['tasks']['todo'] = [t.strip() for t in args.todo.split(",")]

    write_metadata(project_path, meta)
    print(f"Updated metadata for project at {project_path}")

def search_projects(args):
    base_path = args.base_path

    tag = args.tag
    if not tag:
        # Prompt user to select tag with autocomplete
        tags = collect_all_tags(base_path)
        if tags:
            tag = inquirer.fuzzy(
                message="Select tag to filter by (autocomplete):",
                choices=tags,
                multiselect=False,
                instruction="Type to autocomplete, enter to confirm",
            ).execute()
        else:
            tag = None

    projects = find_projects(base_path)
    filtered = filter_projects(projects, tag=tag, stage=args.stage, author=args.author)

    if not filtered:
        print("No projects found matching criteria.")
        return

    for path, meta in filtered:
        progress = summarize_progress(meta)
        print(f"Project: {meta['name']}")
        print(f"Path: {path}")
        print(f"Tags: {', '.join(meta.get('tags', []))}")
        print(f"Stage: {meta['progress']['stage']}")
        print(f"Progress: {progress}\n")

def list_projects_cli(args):
    base_path = args.base_path
    projects = list_projects(base_path)

    if not projects:
        print("No projects or folders found.")
        return

    for p in projects:
        status_symbol = "●" if p["initialized"] else "○"
        #status = "Initialized" if p["initialized"] else "Not initialized"
        tags = ", ".join(p["tags"]) if p["tags"] else "-"
        stage = p["stage"] if p["stage"] else "-"
        #print(f"{p['name']}: {status} | Tags: {tags} | Stage: {stage}")
        print(f"{status_symbol} {p['name']} | Tags: {tags} | Stage: {stage}")

def main():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers()

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize project metadata with interactive prompts")
    parser_init.add_argument("path", nargs="?", default=os.getcwd(), help="Project folder path (default: current directory)")
    parser_init.add_argument("--name", help="Project name")
    parser_init.add_argument("--description", default="", help="Project description")
    parser_init.add_argument("--author", default="", help="Author name")
    parser_init.add_argument("--tags", default="", help="Comma-separated tags")
    parser_init.add_argument("--stage", choices=STAGES, help=f"Stage: {', '.join(STAGES)}")
    parser_init.add_argument(
    "--force", action="store_true",
    help="Force re-initialization by overwriting existing metadata")
    parser_init.set_defaults(func=init_project)

    # Update command
    parser_update = subparsers.add_parser("update", help="Update project metadata")
    parser_update.add_argument("path" , nargs="?", default=os.getcwd(), help="Project folder path (default: current directory)")
    parser_update.add_argument("--name", help="Project name")
    parser_update.add_argument("--description", help="Project description")
    parser_update.add_argument("--author", help="Author name")
    parser_update.add_argument("--tags", help="Comma-separated tags")
    parser_update.add_argument("--completed", help="Comma-separated list of completed tasks")
    parser_update.add_argument("--todo", help="Comma-separated list of todo tasks")
    parser_update.add_argument("--stage", help="Progress stage")
    parser_update.set_defaults(func=update_project)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search projects by criteria")
    parser_search.add_argument("base_path", nargs="?", default=os.getcwd(), help="Base folder to search (default: current directory)")
    parser_search.add_argument("--tag", help="Filter by tag")
    parser_search.add_argument("--stage", help="Filter by stage")
    parser_search.add_argument("--author", help="Filter by author")
    parser_search.set_defaults(func=search_projects)

    #list command
    parser_list = subparsers.add_parser("list", help="List projects and folders in directory")
    parser_list.add_argument("base_path", nargs="?", default=os.getcwd(), help="Directory to list (default: current directory)")
    parser_list.set_defaults(func=list_projects_cli)

    #uninit command
    parser_uninit = subparsers.add_parser("uninit", help="Uninitialize a Tracklet project (remove .projectmeta)")
    parser_uninit.add_argument("path", nargs="?", default=os.getcwd(), help="Project folder path (default: current directory)")
    parser_uninit.set_defaults(func=uninit_project)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
