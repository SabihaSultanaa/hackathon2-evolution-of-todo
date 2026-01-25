"""Toggle command handler for the CLI."""

import argparse

from src.service.task_store import TaskStore


def create_toggle_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Create the 'toggle' subcommand parser.

    Args:
        subparsers: The subparsers action from the main parser.

    Returns:
        The ArgumentParser for the toggle command.
    """
    parser = subparsers.add_parser(
        "toggle",
        help="Toggle task completion",
        description="Mark a task as complete or incomplete.",
    )
    parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="Task ID to toggle (required)",
    )
    return parser


def handle_toggle(args: argparse.Namespace, task_store: TaskStore) -> None:
    """Handle the 'toggle' command.

    Args:
        args: Parsed command-line arguments.
        task_store: The task store to toggle in.
    """
    result = task_store.toggle_task(args.id)

    if result:
        task = task_store.get_task(args.id)
        status = "completed" if task.completed else "pending"
        print(f"Task {args.id} marked as {status}.")
    else:
        print(f"Error: Task {args.id} not found.")
