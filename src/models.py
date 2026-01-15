"""Data models for the To-Do List application.

This module defines the data structures used throughout the application,
including enums for Priority and Status, and the TodoItem class.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Priority(Enum):
    """Priority levels for todo items."""

    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    """Status values for todo items."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (UUID string)
        title: Short description of the task
        details: Detailed description of the task
        priority: Priority level (HIGH, MID, or LOW)
        status: Current status (PENDING or COMPLETED)
        owner: Username of the todo item owner
        created_at: ISO-8601 timestamp of creation
        updated_at: ISO-8601 timestamp of last update
    """

    title: str
    details: str
    priority: Priority
    owner: str
    status: Status = Status.PENDING
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert the TodoItem to a dictionary for JSON serialization.

        Returns:
            Dictionary representation of the TodoItem.
        """
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TodoItem from a dictionary.

        Args:
            data: Dictionary containing todo item data.

        Returns:
            TodoItem instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            details=data["details"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            owner=data["owner"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
