"""
desktop_pet.py

First visual version of Byte.

Responsibilities:
- Display Byte's current state
- Read state from StateManager
- Refresh UI when requested

Future features:
- Images
- Animations
- Notifications
- Interactive buttons
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from Services.state_manager import StateManager


class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.state_manager = StateManager()

        self.setWindowTitle("Enterprise Buddy")
        self.setMinimumWidth(300)

        self.pet_name_label = QLabel()
        self.level_label = QLabel()
        self.hunger_label = QLabel()
        self.energy_label = QLabel()
        self.mood_label = QLabel()
        self.confidence_label = QLabel()

        self.refresh_button = QPushButton("Refresh")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.pet_name_label)
        self.layout.addWidget(self.level_label)
        self.layout.addWidget(self.hunger_label)
        self.layout.addWidget(self.energy_label)
        self.layout.addWidget(self.mood_label)
        self.layout.addWidget(self.confidence_label)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        self.refresh_button.clicked.connect(self.refresh_pet_data)

        self.refresh_pet_data()
        
    def refresh_pet_data(self):
        """
        Reload pet state from disk.
        """
        
        pet = self.state_manager.load_pet_state()
        
        self.pet_name_label.setText(f"🤖 {pet['name']}")
        self.level_label.setText(f"Level: {pet['level']}")
        self.hunger_label.setText(f"Hunger: {pet['hunger']}")
        self.energy_label.setText(f"Energy: {pet['energy']}")
        self.mood_label.setText(f"Mood: {pet['mood']}")
        self.confidence_label.setText(
        f"Confidence: {pet['confidence']}"
        )