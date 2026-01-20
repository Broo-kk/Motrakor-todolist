"""Tests for user authentication functions."""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from main import load_users, save_users


class TestLoadUsers:
    """Tests for loading users."""

    def test_load_users_nonexistent_file(self):
        """Test loading users when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "nonexistent_users.json")
            users = load_users(users_file)
            assert users == []

    def test_load_users_from_existing_file(self):
        """Test loading users from an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            test_users = [
                {"username": "alice", "password": "pass123"},
                {"username": "bob", "password": "pass456"}
            ]
            with open(users_file, 'w') as f:
                json.dump(test_users, f)

            loaded = load_users(users_file)
            assert len(loaded) == 2
            assert loaded[0]["username"] == "alice"
            assert loaded[1]["username"] == "bob"

    def test_load_users_empty_file(self):
        """Test loading users from an empty JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            with open(users_file, 'w') as f:
                json.dump([], f)

            loaded = load_users(users_file)
            assert loaded == []


class TestSaveUsers:
    """Tests for saving users."""

    def test_save_users_creates_file(self):
        """Test that save_users creates a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            users = [{"username": "charlie", "password": "pass789"}]
            
            save_users(users, users_file)
            
            assert os.path.exists(users_file)
            with open(users_file, 'r') as f:
                saved = json.load(f)
            assert saved == users

    def test_save_users_overwrites_existing(self):
        """Test that save_users overwrites existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            old_users = [{"username": "old", "password": "old"}]
            new_users = [{"username": "new", "password": "new"}]
            
            with open(users_file, 'w') as f:
                json.dump(old_users, f)
            
            save_users(new_users, users_file)
            
            with open(users_file, 'r') as f:
                saved = json.load(f)
            assert saved == new_users

    def test_save_empty_users_list(self):
        """Test saving an empty users list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            save_users([], users_file)
            
            with open(users_file, 'r') as f:
                saved = json.load(f)
            assert saved == []


class TestUsersFunctions:
    """Tests for user-related operations."""

    def test_save_and_load_users_roundtrip(self):
        """Test saving and loading users preserves data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            original_users = [
                {"username": "user1", "password": "pwd1"},
                {"username": "user2", "password": "pwd2"}
            ]
            
            save_users(original_users, users_file)
            loaded_users = load_users(users_file)
            
            assert loaded_users == original_users

    def test_load_users_handles_multiple_users(self):
        """Test loading multiple users correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            users = [
                {"username": f"user{i}", "password": f"pass{i}"}
                for i in range(5)
            ]
            with open(users_file, 'w') as f:
                json.dump(users, f)

            loaded = load_users(users_file)
            assert len(loaded) == 5

    def test_save_users_maintains_structure(self):
        """Test that saved users maintain their data structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = os.path.join(tmpdir, "users.json")
            user = {"username": "testuser", "password": "testpass"}
            save_users([user], users_file)
            
            loaded = load_users(users_file)
            assert "username" in loaded[0]
            assert "password" in loaded[0]
            assert loaded[0]["username"] == "testuser"
