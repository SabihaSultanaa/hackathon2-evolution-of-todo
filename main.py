"""Main entry point for the Todo CLI application."""

import sys
from pathlib import Path

# Add src/ to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from service.task_store import TaskStore


def get_string_input(prompt: str, allow_empty: bool = False) -> str:
    """Get a non-empty string input from the user."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  Error: This field cannot be empty. Please try again.")


def get_int_input(prompt: str, min_val: int = 1) -> int:
    """Get a positive integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_val:
                return value
            print(f"  Error: Please enter a number >= {min_val}.")
        except ValueError:
            print("  Error: Please enter a valid number.")


def print_tasks(task_store: TaskStore) -> None:
    """Print all tasks in a formatted table."""
    tasks = task_store.list_tasks()
    if not tasks:
        print("  No tasks found.")
        return

    print()
    print(f"  {'ID':<4} {'Title':<20} {'Description':<30} {'Status':<10}")
    print("  " + "-" * 70)
    for task in tasks:
        status = "Completed" if task.completed else "Pending"
        title = task.title[:20] if len(task.title) > 20 else task.title
        desc = task.description[:30] if len(task.description) > 30 else task.description
        print(f"  {task.id:<4} {title:<20} {desc:<30} {status:<10}")
    print()


def add_task(task_store: TaskStore) -> None:
    """Add a new task."""
    print()
    print("  --- Add New Task ---")
    title = get_string_input("  Title: ")
    description = get_string_input("  Description (optional): ", allow_empty=True)
    task_id = task_store.add_task(title, description)
    print(f"  Task {task_id} created!")
    print()


def view_tasks(task_store: TaskStore) -> None:
    """View all tasks."""
    print()
    print("  --- All Tasks ---")
    print_tasks(task_store)


def toggle_status(task_store: TaskStore) -> None:
    """Toggle a task's completion status."""
    print()
    print("  --- Toggle Task Status ---")
    tasks = task_store.list_tasks()
    if not tasks:
        print("  No tasks to toggle. Add a task first!")
        print()
        return

    print_tasks(task_store)
    task_id = get_int_input("  Enter task ID to toggle: ")
    result = task_store.toggle_task(task_id)
    if result:
        task = task_store.get_task(task_id)
        status = "completed" if task.completed else "pending"
        print(f"  Task {task_id} marked as {status}.")
    else:
        print(f"  Error: Task {task_id} not found.")
    print()


def edit_task(task_store: TaskStore) -> None:
    """Edit an existing task."""
    print()
    print("  --- Edit Task ---")
    tasks = task_store.list_tasks()
    if not tasks:
        print("  No tasks to edit. Add a task first!")
        print()
        return

    print_tasks(task_store)
    task_id = get_int_input("  Enter task ID to edit: ")
    task = task_store.get_task(task_id)
    if task is None:
        print(f"  Error: Task {task_id} not found.")
        print()
        return

    print(f"  Current title: {task.title}")
    print(f"  Current description: {task.description}")
    print()
    print("  Enter new values (leave blank to keep current):")
    new_title = get_string_input("  New title: ", allow_empty=True)
    new_description = get_string_input("  New description: ", allow_empty=True)

    if not new_title and not new_description:
        print("  No changes made.")
        print()
        return

    result = task_store.update_task(
        task_id=task_id,
        title=new_title if new_title else None,
        description=new_description if new_description else None,
    )
    if result:
        print(f"  Task {task_id} updated!")
    else:
        print(f"  Error: Could not update task {task_id}.")
    print()


def delete_task(task_store: TaskStore) -> None:
    """Delete a task."""
    print()
    print("  --- Delete Task ---")
    tasks = task_store.list_tasks()
    if not tasks:
        print("  No tasks to delete. Add a task first!")
        print()
        return

    print_tasks(task_store)
    task_id = get_int_input("  Enter task ID to delete: ")
    result = task_store.delete_task(task_id)
    if result:
        print(f"  Task {task_id} deleted.")
    else:
        print(f"  Error: Task {task_id} not found.")
    print()


def main() -> None:
    """Run the interactive Todo application."""
    print("=" * 40)
    print("       Welcome to TODO APP")
    print("=" * 40)
    print()

    task_store = TaskStore()

    while True:
        print("--- TODO MENU ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Toggle Status")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Exit")
        print()

        choice = get_int_input("Choice (1-6): ", min_val=1)

        if choice == 1:
            add_task(task_store)
        elif choice == 2:
            view_tasks(task_store)
        elif choice == 3:
            toggle_status(task_store)
        elif choice == 4:
            edit_task(task_store)
        elif choice == 5:
            delete_task(task_store)
        elif choice == 6:
            print()
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter 1-6.")
            print()


if __name__ == "__main__":
    main()
