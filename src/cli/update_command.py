"""Update command handler for the CLI."""

import argparse

from src.service.task_store import TaskStore


def create_update_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Create the 'update' subcommand parser.

    Args:
        subparsers: The subparsers action from the main parser.

    Returns:
        The ArgumentParser for the update command.
    """
    parser = subparsers.add_parser(
        "update",
        help="Update a task",
        description="Modify a task's title and/or description by ID.",
    )
    parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="Task ID to update (required)",
    )
    parser.add_argument(
        "--title",
        help="New task title",
    )
    parser.add_argument(
        "--description",
        help="New task description",
    )
    return parser


def handle_update(args: argparse.Namespace, task_store: TaskStore) -> None:
    """Handle the 'update' command.

    Args:
        args: Parsed command-line arguments.
        task_store: The task store to update.
    """
    if args.title is None and args.description is None:
        print("Error: At least one of --title or --description must be provided.")
        return

    result = task_store.update_task(
        task_id=args.id,
        title=args.title,
        description=args.description,
    )

    if result:
        print(f"Task {args.id} updated.")
    else:
        print(f"Error: Task {args.id} not found.")
