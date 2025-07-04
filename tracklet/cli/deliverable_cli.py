import argparse
import os
from pathlib import Path
from tracklet.core.rules_engine import validate_deliverable 
from tracklet.data_access import load_deliverables, save_deliverables, generate_deliverable_id
from tracklet.utils.prompt import is_project_folder
from tracklet.utils.format import print_colored

from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table

console = Console()

def handle_deliverable_add(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    deliverables = load_deliverables(project_path)

    new_deliverable = {
        "id": generate_deliverable_id(),
        "title": args.title,
        "description": args.description or "",
        "due_date": args.due,
        "status": "todo",
        "related_task_id": args.task_id,  # Link to a task if given
        # Add other fields as needed
    }

    valid, errors = validate_deliverable(new_deliverable)
    
    if not valid:
        console.print("[bold red]Deliverable validation failed with errors:[/]")
        for err in errors:
            console.print(f" - [red]{err}[/]")
        return

    deliverables.append(new_deliverable)
    save_deliverables(project_path, deliverables)
    print_colored(f"Deliverable '{new_deliverable['title']}' added successfully with ID {new_deliverable['id']}",color="green", bold=True)

def handle_deliverable_list(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    deliverables = load_deliverables(project_path)
    if not deliverables:
        print_colored("No deliverables found.",color="red")
        return

    # Optionally filter by status, task id etc.
    filtered = deliverables
    if args.status:
        filtered = [d for d in filtered if d.get("status") == args.status]
    if args.task_id:
        filtered = [d for d in filtered if d.get("related_task_id") == args.task_id]

    console = Console()
    table = Table(title="Deliverables")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Due Date", style="red")
    table.add_column("Related Task ID", style="magenta")

    for d in filtered:
        table.add_row(d["id"], d["title"], d["status"], d.get("due_date", "-"), d.get("related_task_id", "-"))

    console.print(table)

def handle_deliverable_update(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    deliverables = load_deliverables(project_path)
    deliverable = next((d for d in deliverables if d["id"] == args.id), None)
    if not deliverable:
        print(f"Deliverable with ID {args.id} not found.")
        return

    updates = {}
    for field in args.fields:
        if '=' not in field:
            print(f"Ignoring invalid field format: '{field}'. Expected key=value.")
            continue
        key, value = field.split('=', 1)
        updates[key.strip()] = value.strip()

    for k, v in updates.items():
        if k in deliverable:
            deliverable[k] = v
        else:
            print(f"Warning: Field '{k}' does not exist on deliverable and was ignored.")

    valid, errors = validate_deliverable(deliverable)
    if not valid:
        print("Deliverable validation failed after update:")
        for err in errors:
            print(f" - {err}")
        return

    save_deliverables(project_path, deliverables)
    print_colored(f"Deliverable '{deliverable['title']}' updated successfully.",color="green")

def handle_deliverable_remove(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    deliverables = load_deliverables(project_path)
    new_deliverables = [d for d in deliverables if d["id"] != args.id]

    if len(new_deliverables) == len(deliverables):
        print_colored(f"No deliverable with ID {args.id} found.",color="red")
        return

    save_deliverables(project_path, new_deliverables)
    print(f"Deliverable with ID {args.id} removed successfully.")

def handle_validate(args):
    deliverables = handle_deliverable_list()
    for d in deliverables:
        valid, errors = validate_deliverable(d)
        status = "✅" if valid else "❌"
        print(f"{status} {d['title']}")
        if errors:
            for err in errors:
                print_colored(f"  - {err}",bold=True)

def register_deliverable_commands(subparsers):
    deliverable = subparsers.add_parser("deliverable", help="Deliverable operations")
    deliverable_sub = deliverable.add_subparsers(dest="deliverable_command", required=True)

    # deliverable add
    parser_deliverable_add = deliverable_sub.add_parser("add", help="Add a new deliverable")
    parser_deliverable_add.add_argument("-t", "--title", required=True, help="Deliverable title")
    parser_deliverable_add.add_argument("-d", "--description", help="Deliverable description")
    parser_deliverable_add.add_argument("--task-id", help="Link to task ID")
    parser_deliverable_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser_deliverable_add.set_defaults(func=handle_deliverable_add)

    # deliverable update
    parser_deliverable_update = deliverable_sub.add_parser("update", help="Update a deliverable")
    parser_deliverable_update.add_argument("id", help="Deliverable ID to update")
    parser_deliverable_update.add_argument("-f", "--fields", nargs="+", help="Fields to update in key=value format")
    parser_deliverable_update.set_defaults(func=handle_deliverable_update)

    # deliverable list
    parser_deliverable_list = deliverable_sub.add_parser("list", help="List deliverables")
    parser_deliverable_list.add_argument("--task-id", help="Filter deliverables by linked task")
    parser_deliverable_list.set_defaults(func=handle_deliverable_list)

    # deliverable remove
    parser_deliverable_remove = deliverable_sub.add_parser("remove", help="Remove a deliverable")
    parser_deliverable_remove.add_argument("id", help="Deliverable ID to remove")
    parser_deliverable_remove.set_defaults(func=handle_deliverable_remove)
