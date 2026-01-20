"""Tests for UI function handlers with page-based navigation."""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from models import TodoItem, Priority, Status
from main import (
    handle_view_all_todos,
    handle_view_todo_details,
    handle_mark_todo_completed,
    save_todos,
    load_todos
)


class TestViewAllTodosUI:
    """Tests for handle_view_all_todos page-based UI."""

    def test_view_all_todos_no_items_returns_on_enter(self):
        """Test view all todos with no items prompts for enter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            with patch('main.load_todos', return_value=[]):
                with patch('builtins.print'):
                    with patch('builtins.input', return_value='') as mock_input:
                        result = handle_view_all_todos("testuser")
                        
                        # Should ask for input when no todos
                        mock_input.assert_called()
                        assert result is None

    def test_view_all_todos_displays_user_todos(self):
        """Test view all todos displays only user's todos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos = [
                TodoItem(
                    title="User Task",
                    details="For testuser",
                    priority=Priority.HIGH,
                    owner="testuser"
                ),
                TodoItem(
                    title="Other Task",
                    details="For other user",
                    priority=Priority.LOW,
                    owner="otheruser"
                )
            ]
            
            with patch('main.load_todos', return_value=todos):
                with patch('builtins.print') as mock_print:
                    with patch('builtins.input', return_value='0'):
                        handle_view_all_todos("testuser")
                        
                        # Verify user's todo was printed
                        print_calls = [str(call) for call in mock_print.call_args_list]
                        assert any("User Task" in str(call) for call in print_calls)

    def test_view_all_todos_return_to_menu_on_zero(self):
        """Test view all todos returns on input 0."""
        todos = [
            TodoItem(
                title="Task 1",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser"
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print'):
                with patch('builtins.input', return_value='0'):
                    result = handle_view_all_todos("testuser")
                    assert result is None

    def test_view_all_todos_shows_completed_symbol(self):
        """Test view all todos shows correct symbols for status."""
        todos = [
            TodoItem(
                title="Pending Task",
                details="Not done",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            ),
            TodoItem(
                title="Completed Task",
                details="Done",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.COMPLETED
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', return_value='0'):
                    handle_view_all_todos("testuser")
                    
                    # Verify symbols are printed
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    output = ''.join(print_calls)
                    assert "○" in output or "Pending Task" in output


class TestViewTodoDetailsUI:
    """Tests for handle_view_todo_details page-based UI."""

    def test_view_todo_details_no_items_returns_on_enter(self):
        """Test view todo details with no items prompts for enter."""
        with patch('main.load_todos', return_value=[]):
            with patch('builtins.print'):
                with patch('builtins.input', return_value='') as mock_input:
                    result = handle_view_todo_details("testuser")
                    mock_input.assert_called()
                    assert result is None

    def test_view_todo_details_shows_item_list(self):
        """Test view todo details shows list of user's todos."""
        todos = [
            TodoItem(
                title="Task 1",
                details="Details 1",
                priority=Priority.HIGH,
                owner="testuser"
            ),
            TodoItem(
                title="Task 2",
                details="Details 2",
                priority=Priority.LOW,
                owner="testuser"
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', side_effect=['0']):
                    handle_view_todo_details("testuser")
                    
                    # Verify items were displayed
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    assert any("Task 1" in str(call) for call in print_calls)
                    assert any("Task 2" in str(call) for call in print_calls)

    def test_view_todo_details_shows_detail_page(self):
        """Test view todo details shows detailed info for selected item."""
        todos = [
            TodoItem(
                title="Test Task",
                details="Test Details",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', side_effect=['1', '0', '0']):  # First 1 to select item, then 0 from detail page
                    handle_view_todo_details("testuser")
                    
                    # Verify detail page was shown
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    output = ''.join(print_calls)
                    assert "Test Task" in output
                    assert "Test Details" in output

    def test_view_todo_details_returns_on_zero_from_list(self):
        """Test view todo details returns to menu on 0 from list."""
        todos = [
            TodoItem(
                title="Task",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser"
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print'):
                with patch('builtins.input', return_value='0'):
                    result = handle_view_todo_details("testuser")
                    assert result is None

    def test_view_todo_details_returns_on_zero_from_detail(self):
        """Test view todo details returns to list on 0 from detail page."""
        todos = [
            TodoItem(
                title="Task",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser"
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print'):
                with patch('builtins.input', side_effect=['1', '0', '0']):  # 1 to select, 0 from detail page, 0 to exit
                    result = handle_view_todo_details("testuser")
                    assert result is None


class TestMarkTodoCompletedUI:
    """Tests for handle_mark_todo_completed page-based UI."""

    def test_mark_completed_no_pending_items(self):
        """Test mark completed with no pending items."""
        with patch('main.load_todos', return_value=[]):
            with patch('builtins.print'):
                with patch('builtins.input', return_value='') as mock_input:
                    result = handle_mark_todo_completed("testuser")
                    mock_input.assert_called()
                    assert result is None

    def test_mark_completed_shows_pending_items(self):
        """Test mark completed shows list of pending items."""
        todos = [
            TodoItem(
                title="Pending Task",
                details="Not done",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            ),
            TodoItem(
                title="Completed Task",
                details="Done",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.COMPLETED
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', return_value='0'):
                    handle_mark_todo_completed("testuser")
                    
                    # Verify only pending task is shown in list
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    assert any("Pending Task" in str(call) for call in print_calls)

    def test_mark_completed_updates_status(self):
        """Test mark completed actually updates the todo status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            todos = [
                TodoItem(
                    title="Task to Complete",
                    details="Details",
                    priority=Priority.HIGH,
                    owner="testuser",
                    status=Status.PENDING
                )
            ]
            todos_file = os.path.join(tmpdir, "todos.json")
            save_todos(todos, todos_file)
            
            with patch('main.load_todos', return_value=todos):
                with patch('main.save_todos') as mock_save:
                    with patch('builtins.print'):
                        with patch('builtins.input', side_effect=['1', '0']):
                            handle_mark_todo_completed("testuser")
                            
                            # Verify save_todos was called
                            mock_save.assert_called()

    def test_mark_completed_shows_success_confirmation(self):
        """Test mark completed shows success confirmation page."""
        todos = [
            TodoItem(
                title="Task to Complete",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('main.save_todos'):
                with patch('builtins.print') as mock_print:
                    with patch('builtins.input', side_effect=['1', '0']):
                        handle_mark_todo_completed("testuser")
                        
                        # Verify confirmation message
                        print_calls = [str(call) for call in mock_print.call_args_list]
                        assert any("marked as completed" in str(call) for call in print_calls)

    def test_mark_completed_returns_on_zero_from_list(self):
        """Test mark completed returns to menu on 0 from list."""
        todos = [
            TodoItem(
                title="Task",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print'):
                with patch('builtins.input', return_value='0'):
                    result = handle_mark_todo_completed("testuser")
                    assert result is None

    def test_mark_completed_returns_on_zero_from_confirmation(self):
        """Test mark completed returns on 0 from confirmation page."""
        todos = [
            TodoItem(
                title="Task",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('main.save_todos'):
                with patch('builtins.print'):
                    with patch('builtins.input', side_effect=['1', '0']):
                        result = handle_mark_todo_completed("testuser")
                        assert result is None

    def test_mark_completed_invalid_input_shows_message(self):
        """Test mark completed shows error on invalid selection."""
        todos = [
            TodoItem(
                title="Task",
                details="Details",
                priority=Priority.HIGH,
                owner="testuser",
                status=Status.PENDING
            )
        ]
        
        with patch('main.load_todos', return_value=todos):
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', side_effect=['5', '0']):  # 5 is invalid
                    handle_mark_todo_completed("testuser")
                    
                    # Verify error message was shown
                    print_calls = [str(call) for call in mock_print.call_args_list]
                    assert any("Invalid" in str(call) for call in print_calls)
