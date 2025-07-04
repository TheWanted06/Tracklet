import argparse
import os
from pathlib import Path
from tracklet.data_access.metadata import create_default_metadata, read_metadata, write_metadata, STAGES, delete_metadata
from tracklet.data_access.tracker import find_projects, filter_projects, summarize_progress, list_projects, collect_all_tags
from tracklet.utils.prompt import prompt_text_list,prompt_multi_select, prompt_tags_with_autocomplete, prompt_text, is_project_folder,prompt_select

from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table


def handle_search(args):
    base_path = os.getcwd()

    # Ensure running in main directory
    if is_project_folder(base_path):
        print("Please run 'tracklet search' from the main projects directory, not inside a project folder.")
        return

    # Find all projects
    projects = find_projects(base_path)
    if not projects:
        print("No projects found.")
        return

    # Initialize filters
    include_filters = {}
    exclude_filters = {}

    # Determine if any filter flags were provided
    flags_provided = any([
        args.name, args.author, args.description,
        args.stage, args.stage_add, args.stage_remove,
        args.tag, args.tag_add, args.tag_remove
    ])

    # If no flags, prompt user interactively to choose filters
    if not flags_provided:
        # Ask which properties to include
        include_props = prompt_multi_select(
            "Select properties to INCLUDE in search:",
            ["name", "author", "description", "stage", "tag"]
        )
        # Ask which properties to exclude
        exclude_props = prompt_multi_select(
            "Select properties to EXCLUDE in search:",
            ["name", "author", "description", "stage", "tag"]
        )
    else:
        include_props = []
        exclude_props = []

    # Helper to get filter values for a property
    def get_filter_values(prop, flag_val, add_flag, remove_flag, all_values):
        values = None
        if flag_val is not None:
            if flag_val == "":
                # Prompt user for values
                if prop in ["stage", "tag"]:
                    values = prompt_multi_select(f"Select {prop}s to filter by:", all_values)
                else:
                    values = prompt_text_list(f"Enter {prop} values (comma-separated):")
            else:
                values = [v.strip() for v in flag_val.split(",") if v.strip()]
        elif prop in include_props:
            # Prompt for include values
            if prop in ["stage", "tag"]:
                values = prompt_multi_select(f"Select {prop}s to INCLUDE:", all_values)
            else:
                values = prompt_text_list(f"Enter {prop} values to INCLUDE (comma-separated):")
        elif prop in exclude_props:
            # Prompt for exclude values
            if prop in ["stage", "tag"]:
                values = prompt_multi_select(f"Select {prop}s to EXCLUDE:", all_values)
            else:
                values = prompt_text_list(f"Enter {prop} values to EXCLUDE (comma-separated):")
        return values

    # Get filter values for each property
    include_filters['name'] = get_filter_values("name", args.name, None, None, [])
    exclude_filters['name'] = None  # No exclude for name in this example

    include_filters['author'] = get_filter_values("author", args.author, None, None, [])
    exclude_filters['author'] = None

    include_filters['description'] = get_filter_values("description", args.description, None, None, [])
    exclude_filters['description'] = None

    include_filters['stage'] = get_filter_values(
        "stage", args.stage_add or args.stage, args.stage_add, args.stage_remove, STAGES
    )
    exclude_filters['stage'] = get_filter_values(
        "stage", args.stage_remove, args.stage_remove, args.stage_remove, STAGES
    )

    #from .tracker import collect_all_tags
    all_tags = collect_all_tags(base_path)
    include_filters['tag'] = get_filter_values(
        "tag", args.tag_add or args.tag, args.tag_add, args.tag_remove, all_tags
    )
    exclude_filters['tag'] = get_filter_values(
        "tag", args.tag_remove, args.tag_remove, args.tag_remove, all_tags
    )

    # Filter projects based on include filters
    filtered = projects
    for prop, values in include_filters.items():
        if values:
            filtered = [
                (path, meta) for path, meta in filtered
                if any(
                    (prop == "tag" and v in meta.get("tags", [])) or
                    (prop == "stage" and v == meta.get("progress", {}).get("stage")) or
                    (prop in meta and v.lower() in str(meta[prop]).lower())
                    for v in values
                )
            ]

    # Apply exclude filters
    for prop, values in exclude_filters.items():
        if values:
            filtered = [
                (path, meta) for path, meta in filtered
                if all(
                    (prop == "tag" and v not in meta.get("tags", [])) and
                    (prop == "stage" and v != meta.get("progress", {}).get("stage")) and
                    (prop not in meta or v.lower() not in str(meta[prop]).lower())
                    for v in values
                )
            ]

    if not filtered:
        print("No projects matched the search criteria.")
        return

    # Display results in Rich table
    console = Console()
    table = Table(title=f"Search Results ({len(filtered)} projects)")

    table.add_column("Project", style="cyan", no_wrap=True)
    table.add_column("Author", style="green")
    table.add_column("Stage", style="magenta")
    table.add_column("Tags", style="yellow")
    table.add_column("Description", style="white")

    for _, meta in filtered:
        tags = ", ".join(meta.get("tags", [])) if meta.get("tags") else "-"
        stage = meta.get("progress", {}).get("stage", "-")
        author = meta.get("author", "-")
        description = meta.get("description", "-")
        name = meta.get("name", "-")
        table.add_row(name, author, stage, tags, description)

    console.print(table)


def handle_list(args):
    base_path = os.getcwd()

    # Check if inside a project directory; if so, warn user
    if os.path.isfile(os.path.join(base_path, ".projectmeta")):
        print("Please run 'tracklet list' from the main projects directory, not inside a project folder.")
        return

    projects = list_projects(base_path)
    if not projects:
        print("No projects found.")
        return

    console = Console()

    if args.detailed:
        table = Table(title=f"Projects in {base_path} (Detailed)")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Stage", style="magenta")
        table.add_column("Tags", style="yellow")

        for p in projects:
            status = "[green]Initialized[/green]" if p["initialized"] else "[red]Not Initialized[/red]"
            stage = p["stage"] or "-"
            tags = ", ".join(p["tags"]) if p["tags"] else "-"
            table.add_row(p["name"], status, stage, tags)

        console.print(table)
    else:
        table = Table(title=f"Projects in {base_path}")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")

        for p in projects:
            status = "[green]✓[/green]" if p["initialized"] else "[red]✗[/red]"
            table.add_row(p["name"], status)

        console.print(table)


def select_project(base_path):
    """Prompt user to select a project folder from base_path."""
    projects = find_projects(base_path)
    if not projects:
        print("No projects found in the current directory.")
        return None

    choices = [
        {"name": f"{meta['name']} ({os.path.basename(path)})", "value": path}
        for path, meta in projects
    ]
    selected = inquirer.select(
        message="Select a project to update:",
        choices=choices,
        cycle=True,
    ).execute()
    return selected

def handle_update(args):
    # Determine project path
    if is_project_folder(os.getcwd()):
        project_path = os.getcwd()
    else:
        project_path = select_project(os.getcwd())
        if not project_path:
            return

    meta = read_metadata(project_path)
    if not meta:
        print("Could not read project metadata.")
        return

    updated = False

    # Update name
    if args.name is not None:
        if args.name == "":
            # Empty string means skip update
            pass
        else:
            new_name = args.name or inquirer.text(
                message=f"Project name [{meta.get('name')}]:",
                default=meta.get('name', '')
            ).execute()
            if new_name != meta.get('name'):
                meta['name'] = new_name
                updated = True

    # Update author
    if args.author is not None:
        new_author = args.author or inquirer.text(
            message=f"Author [{meta.get('author', '')}]:",
            default=meta.get('author', '')
        ).execute()
        if new_author != meta.get('author'):
            meta['author'] = new_author
            updated = True

    # Update description
    if args.description is not None:
        new_desc = args.description or inquirer.text(
            message=f"Description [{meta.get('description', '')}]:",
            default=meta.get('description', '')
        ).execute()
        if new_desc != meta.get('description'):
            meta['description'] = new_desc
            updated = True

    # Update stage
    if args.stage is not None or args.stage_add is not None or args.stage_remove is not None:
        current_stage = meta.get('progress', {}).get('stage', STAGES[0])

        # If stage replace
        if args.stage is not None:
            stage_val = args.stage
            if not stage_val:
                # Prompt if no value
                stage_val = inquirer.select(
                    message="Select project stage:",
                    choices=STAGES,
                    default=current_stage,
                    cycle=True,
                ).execute()
            if stage_val not in STAGES:
                print(f"Invalid stage '{stage_val}'. Please select a valid stage.")
                stage_val = inquirer.select(
                    message="Select project stage:",
                    choices=STAGES,
                    default=current_stage,
                    cycle=True,
                ).execute()
            if stage_val != current_stage:
                meta['progress']['stage'] = stage_val
                updated = True

        # Add/remove stage (optional, usually stage is single-valued)
        # You can implement if your model supports multiple stages

    # Update tags
    tags = meta.get('tags', [])

    # Replace tags
    if args.tag is not None:
        if args.tag == "":
            # Prompt for replacement tags
            new_tags = prompt_tags_with_autocomplete(project_path,"Replace")
        else:
            new_tags = [t.strip() for t in args.tag.split(",") if t.strip()]
        if set(new_tags) != set(tags):
            meta['tags'] = new_tags
            updated = True

    # Add tags
    if args.tag_add is not None:
        if args.tag_add == "":
            add_tags = prompt_tags_with_autocomplete(project_path,"Add")
        else:
            add_tags = [t.strip() for t in args.tag_add.split(",") if t.strip()]
        new_tags = list(set(tags) | set(add_tags))
        if set(new_tags) != set(tags):
            meta['tags'] = new_tags
            updated = True

    # Remove tags
    if args.tag_remove is not None:
        if args.tag_remove == "":
            rem_tags = prompt_tags_with_autocomplete(project_path,"Remove")
        else:
            rem_tags = [t.strip() for t in args.tag_remove.split(",") if t.strip()]
        new_tags = [t for t in tags if t not in rem_tags]
        if set(new_tags) != set(tags):
            meta['tags'] = new_tags
            updated = True

    if updated:
        # Confirm update
        confirm = inquirer.confirm(
            message="Confirm update of project metadata?",
            default=True
        ).execute()
        if confirm:
            write_metadata(project_path, meta)
            print("Project metadata updated successfully.")
        else:
            print("Update cancelled.")
    else:
        print("No changes detected; nothing to update.")


def handle_uninit(args):
    project_path = os.getcwd()

    if not is_project_folder(project_path):
        print("No initialized project found in this directory.")
        return

    if not args.force:
        confirm = inquirer.confirm(
            message="Are you sure you want to uninitialize this project? This will delete the .projectmeta file.",
            default=False
        ).execute()
        if not confirm:
            print("Uninitialization cancelled.")
            return

    try:
        deleted = delete_metadata(project_path)
        if deleted:
            print("Project uninitialized successfully.")
        else:
            print("No .projectmeta file found to delete.")
    except Exception as e:
        print(f"Error deleting .projectmeta file: {e}")


def handle_init(args):
    project_path = os.getcwd()

    # Check if already initialized
    if is_project_folder(project_path):
        print("Project already initialized in this directory.")
        return

    # Prompt for project name, default to current directory name
    default_name = os.path.basename(project_path)
    name = args.name
    if name is None:
        name = inquirer.text(
            message="Project name:",
            default=default_name
        ).execute()

    # Prompt for author
    author = args.author
    if author is None:
        author=prompt_text("Author:")

    # Prompt for description
    description = args.description
    if description is None:
        description = prompt_text("Description:")

    # Prompt for stage with validation
    stage = args.stage
    if stage not in STAGES:
        if stage is not None:
            print(f"Warning: '{stage}' is not a valid stage. Please select from the list.")
        stage = prompt_select(
            "Select project stage:",
            STAGES
        )

    # Prompt for tags (comma-separated)'
    tags = args.tag
    if args.tag:
        tags = [t.strip() for t in args.tag.split(",") if t.strip()]
    else:
        tags = prompt_tags_with_autocomplete(project_path)

    # Create default metadata and write to .projectmeta
    create_default_metadata(project_path, name, description, author, tags, stage)

    print(f"Project initialized successfully in {project_path}")

def register_project_commands(subparsers):
    project_parser = subparsers.add_parser("project", help="Project commands")
    project_sub = project_parser.add_subparsers(dest="command", required=True)

    # init command
    parser_init = project_sub.add_parser("init", help="Initialize a project")
    parser_init.add_argument("-n", "--name", nargs='?', const=None, help="Project name")
    parser_init.add_argument("-a", "--author", nargs='?', const=None, help="Author")
    parser_init.add_argument("-d", "--description", nargs='?', const=None, help="Description")
    parser_init.add_argument("-s", "--stage", nargs='?', const=None, help="Stage")
    parser_init.add_argument("-t", "--tag", nargs='?', const=None, help="Tags (comma-separated)")
    parser_init.set_defaults(func=handle_init)

    # uninit command
    parser_uninit = project_sub.add_parser("uninit", help="Uninitialize a project")
    parser_uninit.add_argument("-f", "--force", action="store_true", help="Force uninit without confirmation")
    parser_uninit.set_defaults(func=handle_uninit)

    # update command
    parser_update = project_sub.add_parser("update", help="Update project metadata")
    parser_update.add_argument("-n", "--name", nargs='?', const=None, help="Project name")
    parser_update.add_argument("-a", "--author", nargs='?', const=None, help="Author")
    parser_update.add_argument("-d", "--description", nargs='?', const=None, help="Description")

    # Stage with add/remove sub-flags
    parser_update.add_argument("-s", "--stage", nargs='?', const=None, help="Stage")
    parser_update.add_argument("-sa", "--stage-add", nargs='?', const=None, help="Add stage (optional)")
    parser_update.add_argument("-sr", "--stage-remove", nargs='?', const=None, help="Remove stage (optional)")

    # Tag with add/remove sub-flags
    parser_update.add_argument("-t", "--tag", nargs='?', const=None, help="Replace tags")
    parser_update.add_argument("-ta", "--tag-add", nargs='?', const=None, help="Add tags")
    parser_update.add_argument("-tr", "--tag-remove", nargs='?', const=None, help="Remove tags")
    parser_update.set_defaults(func=handle_update)

    # list command
    parser_list = project_sub.add_parser("list", help="List projects")
    parser_list.add_argument("-D", "--detailed", action="store_true", help="Show detailed info")
    parser_list.set_defaults(func=handle_list)

    # search command
    parser_search = project_sub.add_parser("search", help="Search projects")
    parser_search.add_argument("-n", "--name", nargs='?', const=None, help="Search by name")
    parser_search.add_argument("-a", "--author", nargs='?', const=None, help="Search by author")
    parser_search.add_argument("-d", "--description", nargs='?', const=None, help="Search by description")

    # Stage search with add/remove include/exclude
    parser_search.add_argument("-s", "--stage", nargs='?', const=None, help="Search by stage")
    parser_search.add_argument("-sa", "--stage-add", nargs='?', const=None, help="Include stages")
    parser_search.add_argument("-sr", "--stage-remove", nargs='?', const=None, help="Exclude stages")

    # Tag search with add/remove include/exclude
    parser_search.add_argument("-t", "--tag", nargs='?', const=None, help="Search by tag")
    parser_search.add_argument("-ta", "--tag-add", nargs='?', const=None, help="Include tags")
    parser_search.add_argument("-tr", "--tag-remove", nargs='?', const=None, help="Exclude tags")
    parser_search.set_defaults(func=handle_search)
