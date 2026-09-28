# Folder Structure

enterprise-buddy/

├── docs/
│
├── data/
│   ├── messages.csv
│   ├── emails.csv
│   ├── tasks.csv
│   ├── meetings.csv
│   ├── manager_requests.csv
│   └── timesheets.csv
│
├── state/
│   ├── pet_state.json
│   └── work_state.json
│
├── prompts/
│   ├── companion_personality.txt
│   └── recommendation_prompt.txt
│
├── services/
│   ├── data_loader.py
│   ├── state_manager.py
│   └── ai_service.py
│
├── engines/
│   ├── context_engine.py
│   ├── pet_health_engine.py
│   ├── recommendation_engine.py
│   └── memory_engine.py
│
├── ui/
│   ├── desktop_pet.py
│   ├── notifications.py
│   └── tray_menu.py
│
├── assets/
│   ├── happy/
│   ├── sad/
│   ├── hungry/
│   └── tired/
│
├── scheduler.py
├── config.py
├── main.py
│
└── requirements.txt