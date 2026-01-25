"""Integration tests for the toggle command in interactive mode."""

import subprocess
import sys


class TestToggleCommand:
    """Test cases for the 'toggle' functionality in interactive mode."""

    def test_toggle_empty_list(self):
        """Test toggling when no tasks exist."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="3\n6\n",  # Toggle Status, then Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "No tasks to toggle" in result.stdout

    def test_toggle_task_not_found(self):
        """Test toggling non-existent task."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n\n3\n99\n6\n",  # Add, Toggle (invalid ID), Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "not found" in result.stdout

    def test_toggle_task(self):
        """Test toggling a task's status."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n\n3\n1\n2\n6\n",  # Add, Toggle, View, Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "completed" in result.stdout
