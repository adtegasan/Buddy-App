"""
state_manager.py

Responsible for:
- Loading application state
- Saving application state
- Creating default state files when needed

This module should remain free of business logic.
"""

from pathlib import Path
import json
from datetime import datetime


class StateManager:
    """
    Handles application persistence.

    Manages:
    - pet_state.json
    - work_state.json
    """

    def __init__(self, state_directory: str = "state"):
        self.state_dir = Path(state_directory)

        self.pet_state_file = self.state_dir / "pet_state.json"
        self.work_state_file = self.state_dir / "work_state.json"

        self._ensure_state_directory()
        self._ensure_state_files()

    def _ensure_state_directory(self) -> None:
        """Create state directory if it does not exist."""
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_state_files(self) -> None:
        """Create default state files if missing."""

        if not self.pet_state_file.exists():
            self.save_pet_state(self.default_pet_state())

        if not self.work_state_file.exists():
            self.save_work_state(self.default_work_state())

    @staticmethod
    def default_pet_state() -> dict:
        """Default pet state."""

        return {
            "name": "Byte",
            "level": 1,
            "experience": 0,
            "hunger": 20,
            "energy": 100,
            "mood": "happy",
            "confidence": 100,
            "status": "healthy",
            "last_updated": datetime.now().isoformat()
        }

    @staticmethod
    def default_work_state() -> dict:
        """Default work state."""

        return {
            "unread_messages": 0,
            "unanswered_emails": 0,
            "overdue_tasks": 0,
            "pending_manager_requests": 0,
            "meetings_today": 0,
            "timesheet_submitted": True,
            "last_updated": datetime.now().isoformat()
        }

    def load_pet_state(self) -> dict:
        """Load pet state."""

        with open(self.pet_state_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_pet_state(self, state: dict) -> None:
        """Save pet state."""

        state["last_updated"] = datetime.now().isoformat()

        with open(self.pet_state_file, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=4)

    def load_work_state(self) -> dict:
        """Load work state."""

        with open(self.work_state_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_work_state(self, state: dict) -> None:
        """Save work state."""

        state["last_updated"] = datetime.now().isoformat()

        with open(self.work_state_file, "w", encoding="utf-8") as file:
            json.dump(state, file, indent=4)

    def reset_pet_state(self) -> dict:
        """Reset pet to defaults."""

        default_state = self.default_pet_state()
        self.save_pet_state(default_state)

        return default_state

    def reset_work_state(self) -> dict:
        """Reset work state to defaults."""

        default_state = self.default_work_state()
        self.save_work_state(default_state)

        return default_state