# Backend

> This is the backend component for the AI Inbox Executive project.

## Structure

```text
backend/
├── database.py          # SQLite + SQLAlchemy setup
├── demo_data.py         # Sample data for demo mode
├── main.py              # Entry point / FastAPI app
├── models.py            # Database models / schemas
├── schemas.py           # Pydantic validation schemas
├── routers/             # API route definitions
│   ├── emails.py
│   ├── followups.py
│   └── tasks.py
└── services/            # External service integrations & business logic
    ├── ai_service.py
    ├── followup_service.py
    ├── gmail_service.py
    └── task_service.py
```

## Key Decisions

* **FastAPI Ecosystem (Framework Choice):** Python and FastAPI were naturally chosen to support asynchronous endpoint generation and Pydantic-based data validation out-of-the-box. This ensures clean, reliable REST API contracts for handling email and task logic without the heavy overhead of bulkier monolith frameworks.
* **Separation of Concerns (Modular Architecture):** The backend is strictly divided into `routers` (for lightweight API endpoint handling) and `services` (for complex business logic, such as OpenAI integration and Google API fetching). This clean modularity allowed for rapid prototyping during the hackathon and keeps the codebase readable.
* **Built-in Mock Environment (Demo Mode):** Since we needed to develop the UI concurrently without constantly pinging external APIs, we built a fallback `demo_data.py` injection pipeline. This allows the backend to serve highly realistic sample emails and mock tasks instantly simply by toggling a `.env` variable, bypassing live Gmail/OpenAI API calls completely.

---

<div align="center">

*Submitted to **IEEE IGNITE Hackathon 2026** — All rights reserved by the respective team.*

</div>
