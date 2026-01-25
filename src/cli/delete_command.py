"""Delete command handler for the CLI."""

import argparse

from src.service.task_store import TaskStore


def create_delete_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Create the 'delete' subcommand parser.

    Args:
        subparsers: The subparsers action from the main parser.

    Returns:
        The ArgumentParser for the delete command.
    """
    parser = subparsers.add_parser(
        "delete",
        help="Delete a task",
        description="Remove a task by its ID.",
    )
    parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="Task ID to delete (required)",
    )
    return parser


def handle_delete(args: argparse.Namespace, task_store: TaskStore) -> None:
    """Handle the 'delete' command.

    Args:
        args: Parsed command-line arguments.
        task_store: The task store to delete from.
    """
    result = task_store.delete_task(args.id)

    if result:
        print(f"Task {args.id} deleted.")
    else:
        print(f"Error: Task {args.id} not found.")
