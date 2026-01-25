"""List command handler for the CLI."""

import argparse

from src.service.task_store import TaskStore


def create_list_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Create the 'list' subcommand parser.

    Args:
        subparsers: The subparsers action from the main parser.

    Returns:
        The ArgumentParser for the list command.
    """
    parser = subparsers.add_parser(
        "list",
        help="List all tasks",
        description="Display all tasks with their ID, title, description, and status.",
    )
    return parser


def handle_list(args: argparse.Namespace, task_store: TaskStore) -> None:
    """Handle the 'list' command.

    Args:
        args: Parsed command-line arguments.
        task_store: The task store to list tasks from.
    """
    tasks = task_store.list_tasks()

    if not tasks:
        print("No tasks found.")
        return

    # Print header
    print(f"{'ID':<4} {'Title':<20} {'Description':<30} {'Status':<10}")
    print("-" * 70)

    # Print each task
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        title = task.title[:20] if len(task.title) > 20 else task.title
        desc = task.description[:30] if len(task.description) > 30 else task.description
        print(f"{task.id:<4} {title:<20} {desc:<30} {status:<10}")
