"""
desktop_pet.py

Enterprise Buddy Desktop Companion
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QProgressBar,
    QApplication,
    QGraphicsDropShadowEffect,
)

from PySide6.QtCore import QTimer, Qt, QPoint
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QBrush, QPen, QFont

from datetime import datetime, timedelta

from Services.state_manager import StateManager
from Services.data_loader import DataLoader

from Engines.context_engine import ContextEngine
from Engines.pet_health_engine import PetHealthEngine

from UI.notifications import NotificationManager
from UI.byte_phrases import get_phrase
from UI.byte_avatar import get_avatar_pixmap


# ── Palette ───────────────────────────────────────────────────────────────────
CARD_BG       = "#13131f"
HEADER_TOP    = "#2d1b69"
HEADER_BTM    = "#13131f"
BORDER        = "#2e2e4e"
TEXT_PRIMARY  = "#e2e8f0"
TEXT_MUTED    = "#7c6fa0"
TEXT_META     = "#4a4a6a"
BUBBLE_BG     = "#1e1e35"
BUBBLE_BORDER = "#3a3a5c"
BUBBLE_TEXT   = "#c4b5fd"
ACCENT        = "#6c63ff"
ACCENT_HOVER  = "#7c74ff"
ACCENT_PRESS  = "#5a52e0"
STAT_TRACK    = "#2e2e4e"

STATUS_COLOURS = {
    "healthy":  "#48bb78",
    "hungry":   "#fc8181",
    "tired":    "#f6ad55",
    "stressed": "#f6ad55",
}

BAR_CONFIG = {
    "hunger":     {"invert": True,  "label": "Hunger"},
    "energy":     {"invert": False, "label": "Energy"},
    "confidence": {"invert": False, "label": "Confidence"},
}

APP_STYLESHEET = f"""
QWidget#root {{
    background: transparent;
}}

QFrame#card {{
    background-color: {CARD_BG};
    border-radius: 20px;
    border: 1px solid {BORDER};
}}

QLabel#pet_name {{
    color: {TEXT_PRIMARY};
    font-size: 20px;
    font-weight: bold;
}}

QLabel#level_mood {{
    color: {TEXT_MUTED};
    font-size: 11px;
    letter-spacing: 1px;
}}

QLabel#stat_label {{
    color: {TEXT_MUTED};
    font-size: 11px;
}}

QLabel#stat_value {{
    color: {TEXT_PRIMARY};
    font-size: 11px;
    font-weight: bold;
}}

QLabel#bubble_text {{
    color: {BUBBLE_TEXT};
    font-size: 12px;
    font-style: italic;
}}

QPushButton#refresh_btn {{
    background-color: {ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 5px 16px;
    font-size: 11px;
    font-weight: bold;
}}

QPushButton#refresh_btn:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton#refresh_btn:pressed {{
    background-color: {ACCENT_PRESS};
}}

QPushButton#close_btn {{
    background-color: rgba(255,255,255,0.08);
    color: {TEXT_MUTED};
    border: none;
    border-radius: 10px;
    font-size: 11px;
    padding: 0px;
}}

QPushButton#close_btn:hover {{
    background-color: rgba(255,255,255,0.15);
    color: {TEXT_PRIMARY};
}}

QLabel#last_updated {{
    color: {TEXT_META};
    font-size: 10px;
}}

QProgressBar {{
    background-color: {STAT_TRACK};
    border-radius: 3px;
    border: none;
    max-height: 6px;
}}

QProgressBar::chunk {{
    border-radius: 3px;
}}
"""


def _bar_colour(value: int, invert: bool) -> str:
    score = (100 - value) if invert else value
    if score >= 70:
        return "#48bb78"
    if score >= 40:
        return "#f6ad55"
    return "#fc8181"


# ── Gradient header ────────────────────────────────────────────────────────────

class _HeaderWidget(QWidget):
    """Top zone of the card — paints a vertical gradient and hosts the avatar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(170)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor(HEADER_TOP))
        grad.setColorAt(1.0, QColor(HEADER_BTM))

        # Clip to top-rounded-only shape (matches card radius at top)
        path = __import__("PySide6.QtGui", fromlist=["QPainterPath"]).QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height() + 20, 20, 20)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QBrush(grad))


# ── Speech bubble with tail ────────────────────────────────────────────────────

class _BubbleWidget(QFrame):
    """Rounded bubble with a small upward-pointing triangle tail."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("bubble_frame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)

        self.label = QLabel("…")
        self.label.setObjectName("bubble_text")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        tail_w, tail_h = 14, 8
        tail_x = w // 2

        path = __import__("PySide6.QtGui", fromlist=["QPainterPath"]).QPainterPath()
        # Tail triangle at top-centre
        path.moveTo(tail_x - tail_w // 2, tail_h)
        path.lineTo(tail_x, 0)
        path.lineTo(tail_x + tail_w // 2, tail_h)
        path.closeSubpath()
        # Bubble body below tail
        path.addRoundedRect(0, tail_h, w, h - tail_h, 12, 12)

        painter.setPen(QPen(QColor(BUBBLE_BORDER), 1))
        painter.setBrush(QBrush(QColor(BUBBLE_BG)))
        painter.drawPath(path)

    def setText(self, text: str):
        self.label.setText(text)

    def sizeHint(self):
        sh = super().sizeHint()
        sh.setHeight(sh.height() + 8)   # account for tail
        return sh


# ── Main widget ────────────────────────────────────────────────────────────────

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.state_manager = StateManager()
        self._last_notification_time = None
        self._drag_pos = QPoint()

        self.data_loader = DataLoader()
        self.context_engine = ContextEngine()
        self.pet_health_engine = PetHealthEngine()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setObjectName("root")
        self.setFixedWidth(320)

        self._build_ui()
        self._apply_shadow()

        QApplication.instance().setStyleSheet(APP_STYLESHEET)

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_pet_data)
        self.timer.start(60000)

        self.refresh_pet_data()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)

        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ── Zone 1: gradient header ────────────────────────────────────────
        self.header = _HeaderWidget()
        header_layout = QVBoxLayout(self.header)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(0)

        # Close button top-right
        top_row = QHBoxLayout()
        top_row.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setObjectName("close_btn")
        close_btn.setFixedSize(22, 22)
        close_btn.clicked.connect(self.close)
        top_row.addWidget(close_btn)
        header_layout.addLayout(top_row)

        # Avatar centred
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.avatar_label)

        # Name + status badge row
        name_row = QHBoxLayout()
        name_row.setAlignment(Qt.AlignCenter)
        self.pet_name_label = QLabel("Byte")
        self.pet_name_label.setObjectName("pet_name")
        self.status_badge = QLabel("HEALTHY")
        self.status_badge.setObjectName("status_badge")
        name_row.addWidget(self.pet_name_label)
        name_row.addSpacing(8)
        name_row.addWidget(self.status_badge)
        header_layout.addLayout(name_row)

        self.level_label = QLabel("LEVEL 1  •  HAPPY")
        self.level_label.setObjectName("level_mood")
        self.level_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.level_label)

        card_layout.addWidget(self.header)

        # ── Zone 2: speech bubble ──────────────────────────────────────────
        bubble_wrapper = QWidget()
        bubble_wrapper.setStyleSheet("background: transparent;")
        bubble_outer = QVBoxLayout(bubble_wrapper)
        bubble_outer.setContentsMargins(18, 4, 18, 0)

        self.bubble = _BubbleWidget()
        bubble_outer.addWidget(self.bubble)
        card_layout.addWidget(bubble_wrapper)

        # ── Zone 3: stats + footer ─────────────────────────────────────────
        stats_widget = QWidget()
        stats_widget.setStyleSheet("background: transparent;")
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(18, 14, 18, 16)
        stats_layout.setSpacing(10)

        # 2-column stat grid
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)

        self.hunger_bar     = self._make_stat_cell(grid, "Hunger",     0, 0)
        self.energy_bar     = self._make_stat_cell(grid, "Energy",     0, 1)
        self.confidence_bar = self._make_stat_cell(grid, "Confidence", 1, 0)

        # Mood in second column of second row
        mood_cell = QVBoxLayout()
        mood_cell.setSpacing(4)
        mood_lbl = QLabel("Mood")
        mood_lbl.setObjectName("stat_label")
        self.mood_label = QLabel("—")
        self.mood_label.setObjectName("stat_value")
        mood_cell.addWidget(mood_lbl)
        mood_cell.addWidget(self.mood_label)
        grid.addLayout(mood_cell, 1, 1)

        stats_layout.addLayout(grid)

        # Thin divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet(f"color: {BORDER}; margin: 0px;")
        stats_layout.addWidget(div)

        # Footer row
        footer = QHBoxLayout()
        self.last_updated_label = QLabel("")
        self.last_updated_label.setObjectName("last_updated")
        refresh_btn = QPushButton("↻  Refresh")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.refresh_pet_data)
        footer.addWidget(self.last_updated_label)
        footer.addStretch()
        footer.addWidget(refresh_btn)
        stats_layout.addLayout(footer)

        card_layout.addWidget(stats_widget)
        root_layout.addWidget(self.card)

    def _make_stat_cell(
        self, grid: QGridLayout, label_text: str, row: int, col: int
    ) -> QProgressBar:
        cell = QVBoxLayout()
        cell.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setObjectName("stat_label")
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setTextVisible(False)
        bar.setFixedHeight(6)
        cell.addWidget(lbl)
        cell.addWidget(bar)
        grid.addLayout(cell, row, col)
        return bar

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.card.setGraphicsEffect(shadow)

    # ── Drag ──────────────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    # ── Notifications ─────────────────────────────────────────────────────────

    def check_notification_conditions(self, context: dict, health: dict):
        reasons = []

        if context["unread_messages"] > 3:
            reasons.append(f"{context['unread_messages']} unread messages")
        if context["pending_manager_requests"] > 0:
            reasons.append(f"{context['pending_manager_requests']} open manager request(s)")
        if context["overdue_tasks"] > 0:
            reasons.append(f"{context['overdue_tasks']} overdue task(s)")
        if not context["timesheet_submitted"]:
            reasons.append("timesheet not submitted")

        if not reasons or health["hunger"] < 50:
            return

        now = datetime.now()
        if (
            self._last_notification_time is not None
            and now - self._last_notification_time < timedelta(minutes=10)
        ):
            return

        self._last_notification_time = now
        message = (
            "Hi, I'm Byte.\n\nI'm getting hungry because:\n\n"
            + "\n".join(f"• {r}" for r in reasons)
        )
        NotificationManager.show_byte_notification("Byte Needs Attention", message)

    # ── Data refresh ──────────────────────────────────────────────────────────

    def refresh_pet_data(self):
        data    = self.data_loader.load_all()
        context = self.context_engine.build_context(data)
        health  = self.pet_health_engine.calculate_pet_health(context)

        self.check_notification_conditions(context, health)

        pet = self.state_manager.load_pet_state()
        pet["hunger"]     = health["hunger"]
        pet["energy"]     = health["energy"]
        pet["confidence"] = health["confidence"]
        pet["mood"]       = health["mood"]
        pet["status"]     = health["status"]
        self.state_manager.save_pet_state(pet)

        self._update_ui(pet)

    def _update_ui(self, pet: dict):
        # Avatar
        self.avatar_label.setPixmap(get_avatar_pixmap(pet["mood"]))

        # Header labels
        self.pet_name_label.setText(pet["name"])
        self.level_label.setText(
            f"LEVEL {pet['level']}  •  {pet['mood'].upper()}"
        )

        # Status badge
        status = pet["status"]
        colour = STATUS_COLOURS.get(status, "#48bb78")
        self.status_badge.setText(f" {status.upper()} ")
        self.status_badge.setStyleSheet(
            f"background-color: {colour}; color: #13131f; "
            "font-size: 10px; font-weight: bold; "
            "padding: 2px 8px; border-radius: 8px;"
        )

        # Stats bars
        bars = {
            "hunger":     self.hunger_bar,
            "energy":     self.energy_bar,
            "confidence": self.confidence_bar,
        }
        for key, bar in bars.items():
            value  = pet[key]
            colour = _bar_colour(value, BAR_CONFIG[key]["invert"])
            bar.setValue(value)
            bar.setStyleSheet(
                f"QProgressBar::chunk {{ background-color: {colour}; border-radius: 3px; }}"
            )

        # Mood text
        self.mood_label.setText(pet["mood"].capitalize())

        # Speech bubble
        self.bubble.setText(get_phrase(pet["mood"], pet["status"]))

        # Footer
        self.last_updated_label.setText(
            f"Updated {datetime.now().strftime('%H:%M')}"
        )
