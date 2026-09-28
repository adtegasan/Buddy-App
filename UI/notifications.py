"""
notifications.py

Responsibilities:
- Show desktop notifications
- Notify user when Byte needs attention
"""

from PySide6.QtWidgets import QMessageBox


class NotificationManager:

    @staticmethod
    def show_byte_notification(title: str, message: str):
        msg = QMessageBox()

        msg.setWindowTitle(title)
        msg.setText(message)

        msg.exec()