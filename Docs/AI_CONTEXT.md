# Master AI Context

You are helping develop Enterprise Buddy.

Enterprise Buddy is a desktop AI companion for corporate workers.

The companion is a pet named Byte.

Byte's health reflects workplace behavior.

Unread messages increase hunger.

Overdue tasks reduce mood.

Meeting overload reduces energy.

Manager requests increase urgency.

Completed work improves health.

The pet must feel supportive and empathetic.

Never guilt the user.

Bad:

"You ignored your tasks."

Good:

"We've got a few things waiting for us."

The application is local only.

Data comes from CSV files.

Technology:

- Python
- PySide6
- Pandas
- JSON
- OpenAI (future)

Architecture:

CSV Data
→ Context Engine
→ Pet Health Engine
→ Recommendation Engine
→ Desktop Pet

The UI should feel like a living desktop companion.