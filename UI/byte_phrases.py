"""
byte_phrases.py

A bank of personality-driven phrases for Byte.
Keyed by (mood, status) tuple.
AI dialogue will replace this in a future version.
"""

import random

# Key: (mood, status)  — both lowercase strings from PetHealthEngine
PHRASES: dict[tuple, list[str]] = {
    ("happy", "healthy"): [
        "All caught up! You're on a roll today. 🌟",
        "Inbox clear, tasks done — I feel great!",
        "Everything looks good from where I'm sitting. Keep it up!",
        "We're in good shape. Nice work today.",
    ],
    ("content", "healthy"): [
        "Things are ticking along nicely. 👍",
        "Not bad at all. A few things in the queue but nothing urgent.",
        "Feeling pretty good. We've got this.",
        "Steady as she goes. Looking good.",
    ],
    ("worried", "hungry"): [
        "I'm getting a little hungry… a few things are piling up.",
        "Some unread messages are starting to bother me. 🥺",
        "We've got a few things waiting for us. Shall we tackle them?",
        "I don't want to nag, but my hunger is creeping up.",
    ],
    ("worried", "stressed"): [
        "A few overdue items have me a bit anxious. No rush — just letting you know.",
        "Feeling a little stretched today. Want to knock something off the list?",
        "Some things have slipped past their due date. We'll get there together.",
        "I'm a bit stressed, but I know we can sort this out.",
    ],
    ("worried", "tired"): [
        "Back-to-back meetings are wearing me out a little. 😴",
        "It's been a busy one. Don't forget to take a breath.",
        "Meeting-heavy day — my energy is dipping.",
        "All those meetings are taking a toll. Almost there!",
    ],
    ("sad", "hungry"): [
        "I'm really hungry now. Things have stacked up quite a bit. 😢",
        "I hate to say it, but I could really use some attention today.",
        "Lots of unread messages and overdue items… I'm struggling a bit.",
        "Please don't forget about me — or the tasks waiting for us.",
    ],
    ("sad", "stressed"): [
        "I'm feeling pretty overwhelmed right now. Let's try to tackle one thing at a time.",
        "The backlog is stressing me out. Even clearing one item would help.",
        "Confidence is low and it shows. We can turn this around together.",
        "It's a tough day, but I believe in us. Let's start somewhere.",
    ],
    ("sad", "tired"): [
        "So many meetings… I'm running on empty. 😪",
        "Energy is low. Maybe block some focus time after this?",
        "I need a breather. Too much on the calendar today.",
        "Feeling drained. Let's see if we can free up some space.",
    ],
}

# Fallback for any combination not explicitly mapped
_FALLBACK = [
    "Just checking in — how's your day going?",
    "I'm here whenever you need me. 😊",
    "Things seem manageable. Let's keep it that way.",
]


def get_phrase(mood: str, status: str) -> str:
    """Return a random phrase for the given mood + status combination."""
    key = (mood.lower(), status.lower())
    options = PHRASES.get(key, _FALLBACK)
    return random.choice(options)
