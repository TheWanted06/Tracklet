import argparse
import os
from pathlib import Path
from .metadata import create_default_metadata, read_metadata, write_metadata, STAGES
from .tracker import find_projects, filter_projects, summarize_progress

def init_project(args):
    project_path = args.path
    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist.")
        return
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    if args.stage and args.stage not in STAGES:
    	print(f"Warning: Stage '{args.stage}' not in predefined stages. Using as is.")
    stage = args.stage if args.stage else "🚧 Planning"
    create_default_metadata(project_path, args.name, args.description, args.author, tags, stage)
    print(f"Initialized project metadata at {project_path}")

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
    projects = find_projects(base_path)
    filtered = filter_projects(projects, tag=args.tag, stage=args.stage, author=args.author)

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

def main():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers()

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize project metadata")
    parser_init.add_argument("path", nargs="?", default=os.getcwd(), 
help="Project folder path (default: current directory)")
    parser_init.add_argument("--name", required=False, default=os.path.basename(os.getcwd()),
 help="Project name (default: current directory name)")
    parser_init.add_argument("--description", default="", help="Project description")
    parser_init.add_argument("--author", default="", help="Author name")
    parser_init.add_argument("--tags", default="", help="Comma-separated tags")
    parser_init.add_argument("--stage", default="🚧 Planning", help="Progress stage")
    parser_init.set_defaults(func=init_project)

    # Update command
    parser_update = subparsers.add_parser("update", help="Update project metadata")
    parser_update.add_argument("path" , nargs="?", default=os.getcwd(), 
help="Project folder path (default: current directory)")
    parser_update.add_argument("--name", help="Project name")
    parser_update.add_argument("--description", help="Project description")
    parser_update.add_argument("--author", help="Author name")
    parser_update.add_argument("--tags", help="Comma-separated tags")
    parser_update.add_argument("--completed", help="Comma-separated list of completed tasks")
    parser_update.add_argument("--todo", help="Comma-separated list of todo tasks")
    parser_update.set_defaults(func=update_project)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search projects by criteria")
    parser_search.add_argument("base_path", nargs="?", default=os.getcwd(), 
help="Base folder to search (default: current directory)")
    parser_search.add_argument("--tag", help="Filter by tag")
    parser_search.add_argument("--stage", help="Filter by stage")
    parser_search.add_argument("--author", help="Filter by author")
    parser_search.set_defaults(func=search_projects)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
