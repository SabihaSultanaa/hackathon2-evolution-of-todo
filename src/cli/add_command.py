"""Add command handler for the CLI."""

import argparse

from src.service.task_store import TaskStore


def create_add_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Create the 'add' subcommand parser.

    Args:
        subparsers: The subparsers action from the main parser.

    Returns:
        The ArgumentParser for the add command.
    """
    parser = subparsers.add_parser(
        "add",
        help="Add a new task",
        description="Create a new task with a title and optional description.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Task title (required)",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Task description (optional)",
    )
    return parser


def handle_add(args: argparse.Namespace, task_store: TaskStore) -> None:
    """Handle the 'add' command.

    Args:
        args: Parsed command-line arguments.
        task_store: The task store to add the task to.
    """
    task_id = task_store.add_task(args.title, args.description)
    print(f"Task {task_id} created: {args.title}")
