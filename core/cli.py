import argparse
import os
from .metadata import create_default_metadata, read_metadata, write_metadata
from .tracker import find_projects, filter_projects, summarize_progress

def init_project(args):
    project_path = args.path
    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist.")
        return
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    create_default_metadata(project_path, args.name, args.description, args.author, tags, args.stage)
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
        meta['progress']['stage'] = args.stage

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
        print(f"Project: {meta['name']}\nPath: {path}\nTags: {', '.join(meta.get('tags', []))}\nStage: {meta['progress']['stage']}\nProgress: {progress}\n")

def main():
    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers()

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize project metadata")
    parser_init.add_argument("path", help="Project folder path")
    parser_init.add_argument("--name", required=True, help="Project name")
    parser_init.add_argument("--description", default="", help="Project description")
    parser_init.add_argument("--author", default="", help="Author name")
    parser_init.add_argument("--tags", default="", help="Comma-separated tags")
    parser_init.add_argument("--stage", default="WIP", help="Progress stage")
    parser_init.set_defaults(func=init_project)

    # Update command
    parser_update = subparsers.add_parser("update", help="Update project metadata")
    parser_update.add_argument("path", help="Project folder path")
    parser_update.add_argument("--name", help="Project name")
    parser_update.add_argument("--description", help="Project description")
    parser_update.add_argument("--author", help="Author name")
    parser_update.add_argument("--tags", help="Comma-separated tags")
    parser_update.add_argument("--stage", help="Progress stage")
    parser_update.set_defaults(func=update_project)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search projects by criteria")
    parser_search.add_argument("base_path", help="Base folder to search projects")
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
