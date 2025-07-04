import argparse
from tracklet.cli.project_cli import register_project_commands
from tracklet.cli.task_cli import register_task_commands
from tracklet.cli.deliverable_cli import register_deliverable_commands

def main():
    parser = argparse.ArgumentParser(prog="tracklet")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_project_commands(subparsers)
    register_task_commands(subparsers)
    register_deliverable_commands(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()    