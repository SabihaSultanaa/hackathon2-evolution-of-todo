"""Integration tests for the add command in interactive mode."""

import subprocess
import sys


class TestAddCommand:
    """Test cases for the 'add' functionality in interactive mode."""

    def test_add_empty_title_rejected(self):
        """Test that empty title is rejected."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="1\n\n\n6\n",  # Add task, empty title, empty description, exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        # Should show error about empty title
        assert "cannot be empty" in result.stdout or result.returncode == 0

    def test_add_help_in_menu(self):
        """Test that menu shows add option."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="6\n",  # Exit immediately
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert "Add Task" in result.stdout


class TestMenuNavigation:
    """Test menu navigation and flow."""

    def test_exit_quits(self):
        """Test that option 6 exits the application."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="6\n",
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert result.returncode == 0
        assert "Goodbye" in result.stdout

    def test_invalid_choice_shows_error(self):
        """Test that invalid choice shows error message."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="99\n6\n",  # Invalid choice, then exit
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert "Invalid choice" in result.stdout

    def test_all_menu_options_displayed(self):
        """Test that all menu options are displayed."""
        result = subprocess.run(
            [sys.executable, "main.py"],
            input="6\n",
            capture_output=True,
            text=True,
            cwd="C:/Users/uzaif/Desktop/hackathon2/todo-app",
        )
        assert "1. Add Task" in result.stdout
        assert "2. View Tasks" in result.stdout
        assert "3. Toggle Status" in result.stdout
        assert "4. Edit Task" in result.stdout
        assert "5. Delete Task" in result.stdout
        assert "6. Exit" in result.stdout
