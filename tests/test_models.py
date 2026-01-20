"""Tests for the TodoItem model and enums."""

import pytest
from models import TodoItem, Priority, Status


class TestPriorityEnum:
    """Tests for the Priority enum."""

    def test_priority_high(self):
        """Test HIGH priority value."""
        assert Priority.HIGH.value == "HIGH"

    def test_priority_mid(self):
        """Test MID priority value."""
        assert Priority.MID.value == "MID"

    def test_priority_low(self):
        """Test LOW priority value."""
        assert Priority.LOW.value == "LOW"


class TestStatusEnum:
    """Tests for the Status enum."""

    def test_status_pending(self):
        """Test PENDING status value."""
        assert Status.PENDING.value == "PENDING"

    def test_status_completed(self):
        """Test COMPLETED status value."""
        assert Status.COMPLETED.value == "COMPLETED"


class TestTodoItem:
    """Tests for the TodoItem class."""

    def test_todo_item_creation(self):
        """Test creating a TodoItem with required fields."""
        todo = TodoItem(
            title="Test Task",
            details="This is a test",
            priority=Priority.HIGH,
            owner="testuser"
        )

        assert todo.title == "Test Task"
        assert todo.details == "This is a test"
        assert todo.priority == Priority.HIGH
        assert todo.owner == "testuser"
        assert todo.status == Status.PENDING

    def test_todo_item_auto_generated_fields(self):
        """Test that id, created_at, and updated_at are auto-generated."""
        todo = TodoItem(
            title="Test Task",
            details="This is a test",
            priority=Priority.MID,
            owner="testuser"
        )

        assert todo.id is not None
        assert len(todo.id) > 0
        assert todo.created_at is not None
        assert todo.updated_at is not None

    def test_todo_item_to_dict(self):
        """Test converting a TodoItem to a dictionary."""
        todo = TodoItem(
            title="Test Task",
            details="Test details",
            priority=Priority.LOW,
            owner="testuser",
            status=Status.COMPLETED
        )

        todo_dict = todo.to_dict()

        assert todo_dict["title"] == "Test Task"
        assert todo_dict["details"] == "Test details"
        assert todo_dict["priority"] == "LOW"
        assert todo_dict["owner"] == "testuser"
        assert todo_dict["status"] == "COMPLETED"
        assert todo_dict["id"] == todo.id

    def test_todo_item_from_dict(self):
        """Test creating a TodoItem from a dictionary."""
        todo_dict = {
            "id": "test-uuid-123",
            "title": "From Dict Task",
            "details": "Created from dict",
            "priority": "HIGH",
            "status": "PENDING",
            "owner": "testuser",
            "created_at": "2025-01-01T10:00:00",
            "updated_at": "2025-01-01T10:00:00"
        }

        todo = TodoItem.from_dict(todo_dict)

        assert todo.id == "test-uuid-123"
        assert todo.title == "From Dict Task"
        assert todo.details == "Created from dict"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "testuser"

    def test_todo_item_round_trip_conversion(self):
        """Test converting TodoItem to dict and back."""
        original_todo = TodoItem(
            title="Round Trip Task",
            details="Testing conversion",
            priority=Priority.MID,
            owner="testuser"
        )

        todo_dict = original_todo.to_dict()
        restored_todo = TodoItem.from_dict(todo_dict)

        assert restored_todo.id == original_todo.id
        assert restored_todo.title == original_todo.title
        assert restored_todo.details == original_todo.details
        assert restored_todo.priority == original_todo.priority
        assert restored_todo.owner == original_todo.owner

    def test_multiple_todos_have_unique_ids(self):
        """Test that multiple TodoItems get unique IDs."""
        todo1 = TodoItem(
            title="Task 1",
            details="Details 1",
            priority=Priority.HIGH,
            owner="user1"
        )
        todo2 = TodoItem(
            title="Task 2",
            details="Details 2",
            priority=Priority.LOW,
            owner="user2"
        )

        assert todo1.id != todo2.id
