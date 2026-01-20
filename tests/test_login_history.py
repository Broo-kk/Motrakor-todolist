"""Tests for login history functionality."""

import pytest
import json
import os
import tempfile
from datetime import datetime
from main import load_login_history, save_login_history, log_login_attempt
from unittest.mock import patch


class TestLoadLoginHistory:
    """Tests for loading login history."""

    def test_load_login_history_nonexistent_file(self):
        """Test loading history when file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "nonexistent_history.json")
            history = load_login_history(history_file)
            assert history == []

    def test_load_login_history_from_existing_file(self):
        """Test loading history from an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            test_data = [
                {"timestamp": "2025-01-01T10:00:00", "username": "user1", "success": True},
                {"timestamp": "2025-01-01T10:05:00", "username": "user2", "success": False}
            ]
            with open(history_file, 'w') as f:
                json.dump(test_data, f)

            loaded = load_login_history(history_file)
            assert len(loaded) == 2
            assert loaded[0]["username"] == "user1"
            assert loaded[0]["success"] is True
            assert loaded[1]["username"] == "user2"
            assert loaded[1]["success"] is False

    def test_load_login_history_empty_file(self):
        """Test loading history from an empty JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            with open(history_file, 'w') as f:
                json.dump([], f)

            loaded = load_login_history(history_file)
            assert loaded == []


class TestSaveLoginHistory:
    """Tests for saving login history."""

    def test_save_login_history_creates_file(self):
        """Test that save_login_history creates a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            record = {"timestamp": "2025-01-01T10:00:00", "username": "testuser", "success": True}
            
            save_login_history([record], history_file)
            
            assert os.path.exists(history_file)
            with open(history_file, 'r') as f:
                saved = json.load(f)
            assert len(saved) == 1
            assert saved[0]["username"] == "testuser"

    def test_save_empty_history(self):
        """Test saving an empty history list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            save_login_history([], history_file)
            
            with open(history_file, 'r') as f:
                saved = json.load(f)
            assert saved == []


class TestLoginHistoryFunctions:
    """Tests for login history operations."""

    def test_save_and_load_history_roundtrip(self):
        """Test saving and loading history preserves data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            original_history = [
                {"timestamp": "2025-01-01T10:00:00", "username": "alice", "success": True},
                {"timestamp": "2025-01-01T10:05:00", "username": "bob", "success": False}
            ]
            
            save_login_history(original_history, history_file)
            loaded = load_login_history(history_file)
            
            assert loaded == original_history

    def test_login_attempt_has_required_fields(self):
        """Test that login attempts include all required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            test_record = {
                "timestamp": "2025-01-01T10:00:00",
                "username": "testuser",
                "success": True
            }
            save_login_history([test_record], history_file)
            
            loaded = load_login_history(history_file)
            record = loaded[0]
            
            assert "timestamp" in record
            assert "username" in record
            assert "success" in record

    def test_log_login_attempt_success(self):
        """Test logging a successful login attempt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            
            def load_mock():
                return load_login_history(history_file)
            
            def save_mock(h):
                save_login_history(h, history_file)
            
            with patch('main.load_login_history', side_effect=load_mock):
                with patch('main.save_login_history', side_effect=save_mock):
                    log_login_attempt("testuser", True)
            
            history = load_login_history(history_file)
            assert len(history) == 1
            assert history[0]["username"] == "testuser"
            assert history[0]["success"] is True

    def test_log_login_attempt_failure(self):
        """Test logging a failed login attempt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            
            def load_mock():
                return load_login_history(history_file)
            
            def save_mock(h):
                save_login_history(h, history_file)
            
            with patch('main.load_login_history', side_effect=load_mock):
                with patch('main.save_login_history', side_effect=save_mock):
                    log_login_attempt("baduser", False)
            
            history = load_login_history(history_file)
            assert len(history) == 1
            assert history[0]["username"] == "baduser"
            assert history[0]["success"] is False

    def test_multiple_login_attempts_logged(self):
        """Test logging multiple login attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            initial = [
                {"timestamp": "2025-01-01T10:00:00", "username": "user1", "success": True}
            ]
            save_login_history(initial, history_file)
            
            def load_mock():
                return load_login_history(history_file)
            
            def save_mock(h):
                save_login_history(h, history_file)
            
            with patch('main.load_login_history', side_effect=load_mock):
                with patch('main.save_login_history', side_effect=save_mock):
                    log_login_attempt("user2", True)
                    log_login_attempt("user3", False)
            
            history = load_login_history(history_file)
            assert len(history) == 3

    def test_login_attempt_timestamp_is_iso_format(self):
        """Test that login attempt timestamps are in ISO-8601 format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = os.path.join(tmpdir, "login_history.json")
            
            def load_mock():
                return load_login_history(history_file)
            
            def save_mock(h):
                save_login_history(h, history_file)
            
            with patch('main.load_login_history', side_effect=load_mock):
                with patch('main.save_login_history', side_effect=save_mock):
                    log_login_attempt("testuser", True)
            
            history = load_login_history(history_file)
            timestamp = history[0]["timestamp"]
            
            try:
                datetime.fromisoformat(timestamp)
                is_valid = True
            except (ValueError, TypeError):
                is_valid = False
            
            assert is_valid
