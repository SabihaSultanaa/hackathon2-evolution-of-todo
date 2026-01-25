"""Integration tests for the update/edit command in interactive mode."""

import subprocess
import sys


class TestUpdateCommand:
    """Test cases for the 'update' functionality in interactive mode."""

    def test_edit_empty_list(self):
        """Test editing when no tasks exist."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="4\n6\n",  # Edit Task, then Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "No tasks to edit" in result.stdout

    def test_edit_task_not_found(self):
        """Test editing non-existent task."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n\n4\n99\n6\n",  # Add, Edit (invalid ID), Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "not found" in result.stdout

    def test_edit_with_changes(self):
        """Test editing a task with new values."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n \n4\n1\nBuy almond milk\nGet almond milk instead\n2\n6\n",  # Add, Edit with changes, View, Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "updated" in result.stdout
        assert "Buy almond milk" in result.stdout
