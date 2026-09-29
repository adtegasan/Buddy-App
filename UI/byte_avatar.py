"""
byte_avatar.py

Generates mood-state SVG avatars for Byte.

When real artwork is ready, replace get_avatar_pixmap() to load
from Assets/{mood}.png instead. No other file needs to change.
"""

from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, Qt

# SVG templates keyed by mood.
# Each mood varies: eye shape, eye-y position, mouth path.
_SVG_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">
  <!-- Body -->
  <rect x="20" y="40" width="80" height="65" rx="16" ry="16" fill="{body}" />
  <!-- Head -->
  <rect x="28" y="10" width="64" height="52" rx="14" ry="14" fill="{head}" />
  <!-- Ear left -->
  <rect x="14" y="22" width="14" height="20" rx="5" ry="5" fill="{head}" />
  <!-- Ear right -->
  <rect x="92" y="22" width="14" height="20" rx="5" ry="5" fill="{head}" />
  <!-- Antenna -->
  <line x1="60" y1="10" x2="60" y2="0" stroke="{accent}" stroke-width="3" stroke-linecap="round"/>
  <circle cx="60" cy="0" r="4" fill="{accent}" />
  <!-- Eyes -->
  {eyes}
  <!-- Mouth -->
  {mouth}
  <!-- Chest panel -->
  <rect x="38" y="55" width="44" height="28" rx="6" ry="6" fill="{panel}" />
  <!-- Panel lights -->
  <circle cx="50" cy="65" r="4" fill="{light1}" />
  <circle cx="60" cy="65" r="4" fill="{light2}" />
  <circle cx="70" cy="65" r="4" fill="{light3}" />
  <!-- Panel bar -->
  <rect x="42" y="74" width="36" height="4" rx="2" fill="{bar_bg}" />
  <rect x="42" y="74" width="{bar_w}" height="4" rx="2" fill="{bar_fill}" />
</svg>
"""

_MOODS = {
    "happy": {
        "body":      "#6c63ff",
        "head":      "#7c74ff",
        "accent":    "#48bb78",
        "panel":     "#1c1c2e",
        "light1":    "#48bb78",
        "light2":    "#48bb78",
        "light3":    "#48bb78",
        "bar_bg":    "#2e2e4e",
        "bar_fill":  "#48bb78",
        "bar_w":     "32",
        "eyes": (
            '<ellipse cx="46" cy="30" rx="7" ry="8" fill="#1c1c2e"/>'
            '<ellipse cx="74" cy="30" rx="7" ry="8" fill="#1c1c2e"/>'
            '<ellipse cx="46" cy="31" rx="4" ry="5" fill="#a78bfa"/>'
            '<ellipse cx="74" cy="31" rx="4" ry="5" fill="#a78bfa"/>'
        ),
        "mouth": '<path d="M44 48 Q60 58 76 48" stroke="#1c1c2e" stroke-width="3" fill="none" stroke-linecap="round"/>',
    },
    "content": {
        "body":      "#5a52c8",
        "head":      "#6a62d8",
        "accent":    "#90cdf4",
        "panel":     "#1c1c2e",
        "light1":    "#90cdf4",
        "light2":    "#90cdf4",
        "light3":    "#2e2e4e",
        "bar_bg":    "#2e2e4e",
        "bar_fill":  "#90cdf4",
        "bar_w":     "22",
        "eyes": (
            '<ellipse cx="46" cy="31" rx="7" ry="7" fill="#1c1c2e"/>'
            '<ellipse cx="74" cy="31" rx="7" ry="7" fill="#1c1c2e"/>'
            '<ellipse cx="46" cy="32" rx="4" ry="4" fill="#a78bfa"/>'
            '<ellipse cx="74" cy="32" rx="4" ry="4" fill="#a78bfa"/>'
        ),
        "mouth": '<line x1="46" y1="50" x2="74" y2="50" stroke="#1c1c2e" stroke-width="3" stroke-linecap="round"/>',
    },
    "worried": {
        "body":      "#7c5cd8",
        "head":      "#8c6ce8",
        "accent":    "#f6ad55",
        "panel":     "#1c1c2e",
        "light1":    "#f6ad55",
        "light2":    "#2e2e4e",
        "light3":    "#2e2e4e",
        "bar_bg":    "#2e2e4e",
        "bar_fill":  "#f6ad55",
        "bar_w":     "14",
        "eyes": (
            # Slightly raised inner corners = worried brow
            '<ellipse cx="46" cy="33" rx="7" ry="6" fill="#1c1c2e"/>'
            '<ellipse cx="74" cy="33" rx="7" ry="6" fill="#1c1c2e"/>'
            '<ellipse cx="46" cy="34" rx="4" ry="3.5" fill="#c4b5fd"/>'
            '<ellipse cx="74" cy="34" rx="4" ry="3.5" fill="#c4b5fd"/>'
            '<line x1="40" y1="25" x2="51" y2="28" stroke="#8c6ce8" stroke-width="2.5" stroke-linecap="round"/>'
            '<line x1="80" y1="25" x2="69" y2="28" stroke="#8c6ce8" stroke-width="2.5" stroke-linecap="round"/>'
        ),
        "mouth": '<path d="M46 52 Q60 46 74 52" stroke="#1c1c2e" stroke-width="3" fill="none" stroke-linecap="round"/>',
    },
    "sad": {
        "body":      "#4a3fa0",
        "head":      "#5a4fb0",
        "accent":    "#fc8181",
        "panel":     "#1c1c2e",
        "light1":    "#fc8181",
        "light2":    "#2e2e4e",
        "light3":    "#2e2e4e",
        "bar_bg":    "#2e2e4e",
        "bar_fill":  "#fc8181",
        "bar_w":     "8",
        "eyes": (
            # Drooped eyes + strong worry brows
            '<ellipse cx="46" cy="35" rx="6" ry="5" fill="#1c1c2e"/>'
            '<ellipse cx="74" cy="35" rx="6" ry="5" fill="#1c1c2e"/>'
            '<ellipse cx="46" cy="36" rx="3.5" ry="3" fill="#c4b5fd"/>'
            '<ellipse cx="74" cy="36" rx="3.5" ry="3" fill="#c4b5fd"/>'
            '<line x1="39" y1="24" x2="52" y2="29" stroke="#5a4fb0" stroke-width="3" stroke-linecap="round"/>'
            '<line x1="81" y1="24" x2="68" y2="29" stroke="#5a4fb0" stroke-width="3" stroke-linecap="round"/>'
        ),
        "mouth": '<path d="M44 54 Q60 44 76 54" stroke="#1c1c2e" stroke-width="3" fill="none" stroke-linecap="round"/>',
    },
}


def get_avatar_pixmap(mood: str, size: int = 110) -> QPixmap:
    """
    Return a QPixmap of Byte for the given mood state.

    Swap this function body to load from Assets/{mood}.png
    when real artwork is available.
    """
    config = _MOODS.get(mood.lower(), _MOODS["content"])
    svg_str = _SVG_TEMPLATE.format(**config)

    renderer = QSvgRenderer(QByteArray(svg_str.encode()))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap
