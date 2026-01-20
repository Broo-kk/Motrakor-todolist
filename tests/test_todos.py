"""Tests for todo item management functions."""

import pytest
import json
import os
import tempfile
from models import TodoItem, Priority, Status
from main import load_todos, save_todos


class TestLoadTodos:
    """Tests for loading todo items."""

    def test_load_todos_nonexistent_file(self):
        """Test loading todos when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "nonexistent_todos.json")
            todos = load_todos(todos_file)
            assert todos == []

    def test_load_todos_from_existing_file(self):
        """Test loading todos from an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            test_data = [
                {
                    "id": "uuid-1",
                    "title": "Task 1",
                    "details": "Details 1",
                    "priority": "HIGH",
                    "status": "PENDING",
                    "owner": "user1",
                    "created_at": "2025-01-01T10:00:00",
                    "updated_at": "2025-01-01T10:00:00"
                }
            ]
            with open(todos_file, 'w') as f:
                json.dump(test_data, f)

            loaded = load_todos(todos_file)
            assert len(loaded) == 1
            assert isinstance(loaded[0], TodoItem)
            assert loaded[0].title == "Task 1"
            assert loaded[0].priority == Priority.HIGH

    def test_load_todos_empty_file(self):
        """Test loading todos from an empty JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            with open(todos_file, 'w') as f:
                json.dump([], f)

            loaded = load_todos(todos_file)
            assert loaded == []


class TestSaveTodos:
    """Tests for saving todo items."""

    def test_save_todos_creates_file(self):
        """Test that save_todos creates a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            todo = TodoItem(
                title="New Task",
                details="Details",
                priority=Priority.HIGH,
                owner="user1"
            )
            
            save_todos([todo], todos_file)
            
            assert os.path.exists(todos_file)
            with open(todos_file, 'r') as f:
                saved = json.load(f)
            assert len(saved) == 1
            assert saved[0]["title"] == "New Task"

    def test_save_todos_converts_enums(self):
        """Test that save_todos converts enums to strings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            todo = TodoItem(
                title="Test",
                details="Details",
                priority=Priority.HIGH,
                owner="user",
                status=Status.COMPLETED
            )
            
            save_todos([todo], todos_file)
            
            with open(todos_file, 'r') as f:
                saved = json.load(f)
            assert saved[0]["priority"] == "HIGH"
            assert saved[0]["status"] == "COMPLETED"

    def test_save_empty_todos_list(self):
        """Test saving an empty todos list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            save_todos([], todos_file)
            
            with open(todos_file, 'r') as f:
                saved = json.load(f)
            assert saved == []


class TestTodosFunctions:
    """Tests for todo-related operations."""

    def test_save_and_load_todos_roundtrip(self):
        """Test saving and loading todos preserves data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            original_todos = [
                TodoItem(
                    title="Important Task",
                    details="High priority work",
                    priority=Priority.HIGH,
                    owner="alice",
                    status=Status.PENDING
                ),
                TodoItem(
                    title="Completed Task",
                    details="Already done",
                    priority=Priority.MID,
                    owner="bob",
                    status=Status.COMPLETED
                )
            ]
            
            save_todos(original_todos, todos_file)
            loaded = load_todos(todos_file)
            
            assert len(loaded) == 2
            assert loaded[0].title == original_todos[0].title
            assert loaded[1].status == Status.COMPLETED

    def test_load_todos_preserves_priority_enums(self):
        """Test that loading todos correctly converts priorities."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            test_data = [
                {
                    "id": "uuid-123",
                    "title": "Test",
                    "details": "Details",
                    "priority": "LOW",
                    "status": "PENDING",
                    "owner": "user",
                    "created_at": "2025-01-01T10:00:00",
                    "updated_at": "2025-01-01T10:00:00"
                }
            ]
            with open(todos_file, 'w') as f:
                json.dump(test_data, f)

            loaded = load_todos(todos_file)
            assert isinstance(loaded[0].priority, Priority)
            assert loaded[0].priority == Priority.LOW

    def test_load_todos_preserves_status_enums(self):
        """Test that loading todos correctly converts statuses."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            test_data = [
                {
                    "id": "uuid-456",
                    "title": "Test",
                    "details": "Details",
                    "priority": "HIGH",
                    "status": "COMPLETED",
                    "owner": "user",
                    "created_at": "2025-01-01T10:00:00",
                    "updated_at": "2025-01-01T10:00:00"
                }
            ]
            with open(todos_file, 'w') as f:
                json.dump(test_data, f)

            loaded = load_todos(todos_file)
            assert isinstance(loaded[0].status, Status)
            assert loaded[0].status == Status.COMPLETED

    def test_multiple_todos_for_same_user(self):
        """Test saving and loading multiple todos for same user."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            todos = [
                TodoItem(
                    title=f"Task {i}",
                    details=f"Details {i}",
                    priority=Priority.HIGH,
                    owner="alice"
                )
                for i in range(3)
            ]
            
            save_todos(todos, todos_file)
            loaded = load_todos(todos_file)
            
            assert len(loaded) == 3
            assert all(todo.owner == "alice" for todo in loaded)

    def test_todos_maintain_ids_after_roundtrip(self):
        """Test that todos maintain unique IDs after save/load."""
        with tempfile.TemporaryDirectory() as tmpdir:
            todos_file = os.path.join(tmpdir, "todos.json")
            original_todo = TodoItem(
                title="Unique Task",
                details="Test",
                priority=Priority.LOW,
                owner="user"
            )
            original_id = original_todo.id
            
            save_todos([original_todo], todos_file)
            loaded = load_todos(todos_file)
            
            assert loaded[0].id == original_id
