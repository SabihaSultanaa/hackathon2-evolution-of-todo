"""Integration tests for the list/view command in interactive mode."""

import subprocess
import sys


class TestListCommand:
    """Test cases for the 'list' functionality in interactive mode."""

    def test_view_empty_list(self):
        """Test viewing when no tasks exist."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="2\n6\n",  # View Tasks, then Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "No tasks found" in result.stdout

    def test_view_with_task(self):
        """Test viewing with a task."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\nBuy milk\n\n2\n6\n",  # Add, View, Exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "Buy milk" in result.stdout
        assert "Pending" in result.stdout
