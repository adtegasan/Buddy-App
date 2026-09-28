# System Architecture

## High Level Architecture

CSV Data
    ↓
Data Loader
    ↓
Context Engine
    ↓
Pet Health Engine
    ↓
Recommendation Engine
    ↓
Desktop Pet UI

---

## Components

### Data Layer

Mock enterprise data.

Files:

- messages.csv
- emails.csv
- tasks.csv
- meetings.csv
- manager_requests.csv
- timesheets.csv

---

### Context Engine

Responsibility:

Convert raw data into workplace context.

Example:

- unread messages
- overdue tasks
- pending requests

---

### Pet Health Engine

Responsibility:

Transform work context into companion wellbeing.

Outputs:

- hunger
- mood
- energy
- confidence

---

### Recommendation Engine

Responsibility:

Determine the most important guidance to provide.

Uses:

- work context
- pet health

---

### AI Layer

Responsibility:

Generate personality-driven language.

AI should never calculate business logic.

AI only generates wording.

---

### UI Layer

Responsibility:

Display:

- Pet
- Mood
- Notifications
- Interactions

The UI should resemble a companion, not a dashboard.