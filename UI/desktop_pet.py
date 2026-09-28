"""
desktop_pet.py

Enterprise Buddy Desktop Companion

Responsibilities:
- Display Byte's current state
- Load enterprise data
- Build work context
- Calculate pet health
- Display notifications
- Refresh automatically

Future features:
- Images
- Animations
- AI-generated dialogue
- Interactive pet actions
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtCore import QTimer

from Services.state_manager import StateManager
from Services.data_loader import DataLoader

from Engines.context_engine import ContextEngine
from Engines.pet_health_engine import PetHealthEngine

from UI.notifications import NotificationManager


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.state_manager = StateManager()

        self.data_loader = DataLoader()
        self.context_engine = ContextEngine()
        self.pet_health_engine = PetHealthEngine()

        self.setWindowTitle("Enterprise Buddy")
        self.setMinimumWidth(350)

        self.pet_name_label = QLabel()
        self.level_label = QLabel()
        self.hunger_label = QLabel()
        self.energy_label = QLabel()
        self.mood_label = QLabel()
        self.confidence_label = QLabel()
        self.status_label = QLabel()

        self.refresh_button = QPushButton("Refresh")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.pet_name_label)
        self.layout.addWidget(self.level_label)
        self.layout.addWidget(self.hunger_label)
        self.layout.addWidget(self.energy_label)
        self.layout.addWidget(self.mood_label)
        self.layout.addWidget(self.confidence_label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        self.refresh_button.clicked.connect(
            self.refresh_pet_data
        )

        # Auto refresh every 60 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(
            self.refresh_pet_data
        )
        self.timer.start(60000)

        self.refresh_pet_data()

    def check_notification_conditions(
        self,
        context: dict,
        health: dict
    ):
        """
        Determine whether Byte should
        show a notification.
        """

        reasons = []

        if context["unread_messages"] > 3:
            reasons.append(
                f"{context['unread_messages']} unread messages"
            )

        if context["pending_manager_requests"] > 0:
            reasons.append(
                f"{context['pending_manager_requests']} open manager request(s)"
            )

        if context["overdue_tasks"] > 0:
            reasons.append(
                f"{context['overdue_tasks']} overdue task(s)"
            )

        if not context["timesheet_submitted"]:
            reasons.append(
                "timesheet not submitted"
            )

        if not reasons:
            return

        if health["hunger"] < 50:
            return

        message = (
            "Hi, I'm Byte.\n\n"
            "I'm getting hungry because:\n\n"
            + "\n".join(
                f"• {reason}"
                for reason in reasons
            )
        )

        NotificationManager.show_byte_notification(
            "Byte Needs Attention",
            message
        )

    def refresh_pet_data(self):
        """
        Refresh Byte using current
        enterprise work data.
        """

        data = self.data_loader.load_all()

        context = self.context_engine.build_context(
            data
        )

        health = self.pet_health_engine.calculate_pet_health(
            context
        )

        self.check_notification_conditions(
            context,
            health
        )

        pet = self.state_manager.load_pet_state()

        pet["hunger"] = health["hunger"]
        pet["energy"] = health["energy"]
        pet["confidence"] = health["confidence"]
        pet["mood"] = health["mood"]
        pet["status"] = health["status"]

        self.state_manager.save_pet_state(pet)

        self.pet_name_label.setText(
            f"🤖 {pet['name']}"
        )

        self.level_label.setText(
            f"Level: {pet['level']}"
        )

        self.hunger_label.setText(
            f"Hunger: {pet['hunger']}"
        )

        self.energy_label.setText(
            f"Energy: {pet['energy']}"
        )

        self.mood_label.setText(
            f"Mood: {pet['mood']}"
        )

        self.confidence_label.setText(
            f"Confidence: {pet['confidence']}"
        )

        self.status_label.setText(
            f"Status: {pet['status']}"
        )