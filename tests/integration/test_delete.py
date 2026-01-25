"""Integration tests for the delete command in interactive mode."""

import subprocess
import sys


class TestDeleteCommand:
    """Test cases for the 'delete' functionality in interactive mode."""

    def test_delete_empty_list(self):
        """Test deleting when no tasks exist."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="5\n6\n",  # Delete Task, then Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "No tasks to delete" in result.stdout

    def test_delete_task_not_found(self):
        """Test deleting non-existent task."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n\n5\n99\n6\n",  # Add, Delete (invalid ID), Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "not found" in result.stdout

    def test_delete_task(self):
        """Test deleting a task."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n \n5\n1\n2\n6\n",  # Add (with space for empty desc), Delete task 1, View, Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "deleted" in result.stdout
        # After deletion, view should show no tasks
        assert "No tasks" in result.stdout or "Buy milk" not in result.stdout
