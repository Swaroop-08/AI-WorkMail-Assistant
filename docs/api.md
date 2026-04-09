# API Documentation

> This document details the RESTful API endpoints exposed by the FastAPI backend.

## Base URL
All API requests should be prefixed exactly with:
`http://localhost:8000/api` (or your deployed equivalent).

---

## 📧 Emails

### `GET /api/emails`
Fetches a list of emails (either from the live Gmail API or Demo generator).
**Response:**
```json
[
  {
    "id": "1",
    "subject": "Project Update",
    "sender": "boss@company.com",
    "snippet": "Don't forget the meeting tomorrow...",
    "isRead": false,
    "intent": "Actionable"
  }
]
```

### `GET /api/emails/{email_id}`
Gets the detailed data of a specific email, including AI-generated reply suggestions.

---

## ✅ Tasks

### `GET /api/tasks`
Returns all extracted tasks to populate the Kanban board.
**Response:**
```json
[
  {
    "id": "101",
    "title": "Review Slide Deck",
    "status": "todo",
    "priority": "high",
    "dueDate": "2026-04-10"
  }
]
```

### `POST /api/tasks`
Manually create a new task.

### `PUT /api/tasks/{task_id}/status`
Updates the Kanban status (`todo`, `in_progress`, `done`) of a specific task.

---

## 🔔 Follow-ups

### `GET /api/followups`
Retrieves a list of emails sent over 24 hours ago that have received no reply.

---

*For interactive Swagger UI documentation, visit `http://localhost:8000/docs` while the server is running.*

---

<div align="center">

*Submitted to **IEEE IGNITE Hackathon 2026** — All rights reserved by the respective team.*

</div>
