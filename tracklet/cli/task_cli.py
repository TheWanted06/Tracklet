import argparse
import os
from pathlib import Path
from tracklet.data_access import load_deliverables, save_deliverables, generate_deliverable_id, load_tasks, save_tasks, generate_task_id
from tracklet.core.rules_engine import validate_task
from tracklet.utils import is_project_folder, prompt_tags_with_autocomplete
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table

def handle_task_add(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    # Load existing tasks
    tasks = load_tasks(project_path)

    # Create new task dict
    new_task = {
        "id": generate_task_id(),
        "title": args.title,
        "description": args.description or "",
        "priority": args.priority,
        "assignees": args.assignees or [],
        "due_date": args.due,
        "status": "todo",  # default initial status
        "tags": [],
        # Add more fields as necessary, e.g. timestamps
    }

    # Run pre-task rules (example, assuming you have a validate_task function)
    
    valid, errors = validate_task(new_task)
    if not valid:
        print("Task validation failed with errors:")
        for err in errors:
            print(f" - {err}")
        return

    # Append and save
    tasks.append(new_task)
    save_tasks(project_path, tasks)
    print(f"Task '{new_task['title']}' added successfully with ID {new_task['id']}")


def handle_task_update(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    tasks = load_tasks(project_path)
    task = next((t for t in tasks if t["id"] == args.id), None)
    if not task:
        print(f"Task with ID {args.id} not found.")
        return

    # Parse fields key=value pairs
    updates = {}
    for field in args.fields:
        if '=' not in field:
            print(f"Ignoring invalid field format: '{field}'. Expected key=value.")
            continue
        key, value = field.split('=', 1)
        updates[key.strip()] = value.strip()

    # Update task fields
    for k, v in updates.items():
        if k in task:
            task[k] = v
        else:
            print(f"Warning: Field '{k}' does not exist on task and was ignored.")

    # Run post-update validation if needed
    from tracklet.core.rules_engine import validate_task
    valid, errors = validate_task(task)
    if not valid:
        print("Task validation failed after update:")
        for err in errors:
            print(f" - {err}")
        return

    save_tasks(project_path, tasks)
    print(f"Task '{task['title']}' updated successfully.")


def handle_task_list(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    tasks = load_tasks(project_path)
    if not tasks:
        print("No tasks found.")
        return

    # Apply filters if any
    filtered = tasks
    if args.status:
        filtered = [t for t in filtered if t.get("status") == args.status]
    if args.priority:
        filtered = [t for t in filtered if t.get("priority") == args.priority]
    if args.tag:
        filtered = [t for t in filtered if args.tag in t.get("tags", [])]

    # Display tasks using rich Table
    console = Console()
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Priority", style="magenta")
    table.add_column("Status", style="yellow")
    table.add_column("Due Date", style="red")

    for t in filtered:
        table.add_row(t["id"], t["title"], t["priority"], t["status"], t.get("due_date", "-"))

    console.print(table)

def handle_task_remove(args):
    project_path = Path.cwd()
    if not is_project_folder(project_path):
        print("Error: Not inside a valid project folder.")
        return

    tasks = load_tasks(project_path)
    new_tasks = [t for t in tasks if t["id"] != args.id]

    if len(new_tasks) == len(tasks):
        print(f"No task with ID {args.id} found.")
        return

    save_tasks(project_path, new_tasks)
    print(f"Task with ID {args.id} removed successfully.")

def register_task_commands(subparsers):
    parser_task = subparsers.add_parser("task", help="Manage tasks")
    task_sub = parser_task.add_subparsers(dest="task_command", required=True)

    # task add
    parser_task_add = task_sub.add_parser("add", help="Add a new task")
    parser_task_add.add_argument("-t", "--title", required=True, help="Task title")
    parser_task_add.add_argument("-d", "--description", help="Task description")
    parser_task_add.add_argument("-p", "--priority", choices=["low", "medium", "high", "critical"], default="medium")
    parser_task_add.add_argument("-a", "--assignees", nargs="*", help="Assignees emails/usernames")
    parser_task_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser_task_add.set_defaults(func=handle_task_add)

    # task update
    parser_task_update = task_sub.add_parser("update", help="Update a task")
    parser_task_update.add_argument("id", help="Task ID to update")
    parser_task_update.add_argument("-f", "--fields", nargs="+", help="Fields to update in key=value format")
    parser_task_update.set_defaults(func=handle_task_update)

    # task list
    parser_task_list = task_sub.add_parser("list", help="List tasks")
    parser_task_list.add_argument("-s", "--status", help="Filter by status")
    parser_task_list.add_argument("-p", "--priority", help="Filter by priority")
    parser_task_list.add_argument("-t", "--tag", help="Filter by tag")
    parser_task_list.set_defaults(func=handle_task_list)

    # task remove
    parser_task_remove = task_sub.add_parser("remove", help="Remove a task")
    parser_task_remove.add_argument("id", help="Task ID to remove")
    parser_task_remove.set_defaults(func=handle_task_remove)
