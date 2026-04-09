"""
AI Service — GPT-powered email classification, task extraction, and suggestion generation.
Falls back to demo responses when DEMO_MODE is enabled or OpenAI key is missing.
"""
import os
import json
from typing import Dict, List, Optional

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def _get_client():
    """Get OpenAI client."""
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY)


def _is_ai_available() -> bool:
    """Check if AI service is available."""
    return not DEMO_MODE and bool(OPENAI_API_KEY)


def classify_email(subject: str, body: str) -> Dict:
    """
    Classify an email into actionable/informational and detect intent.
    Returns: {classification, intent, priority}
    """
    if not _is_ai_available():
        return _mock_classify(subject, body)

    client = _get_client()

    system_prompt = """You are an expert email analyst. Analyze the given email and return a JSON object with:
1. "classification": either "actionable" or "informational"
   - "actionable": requires the recipient to DO something (reply, attend, complete a task, send something)
   - "informational": does NOT require action (newsletters, notifications, FYI messages)

2. "intent": one of these values:
   - "reply_required": the sender expects a written response
   - "schedule_meeting": involves scheduling, calendar events, meetings
   - "send_document": involves sharing/sending/reviewing documents or files
   - "follow_up_needed": references a previous conversation that needs continuation
   - "general": doesn't fit the above categories

3. "priority": one of "high", "medium", "low"
   - "high": urgent, has a close deadline, or involves important stakeholders
   - "medium": important but not urgent
   - "low": can be addressed later, newsletters, FYI

Respond ONLY with valid JSON. No extra text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Subject: {subject}\n\nBody:\n{body[:2000]}"},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return {
            "classification": result.get("classification", "informational"),
            "intent": result.get("intent", "general"),
            "priority": result.get("priority", "medium"),
        }
    except Exception as e:
        print(f"AI classification error: {e}")
        return _mock_classify(subject, body)


def extract_tasks(subject: str, body: str, sender: str) -> List[Dict]:
    """
    Extract structured tasks from an email.
    Returns: [{task_type, description, deadline, people_involved, priority}]
    """
    if not _is_ai_available():
        return _mock_extract_tasks(subject, body, sender)

    client = _get_client()

    system_prompt = """You are a task extraction assistant. Analyze the email and extract ALL actionable tasks.

For each task, return a JSON object in an array with these fields:
- "task_type": a short category (e.g., "Reply", "Schedule Meeting", "Review Document", "Send Document", "Complete Form", "Fix Issue")
- "description": a clear, concise description of what needs to be done
- "deadline": when it's due (extract from the email, or "Not specified")
- "people_involved": comma-separated names of people involved
- "priority": "high", "medium", or "low"

Return a JSON object with key "tasks" containing the array.
If no actionable tasks are found, return {"tasks": []}.
Respond ONLY with valid JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Subject: {subject}\nFrom: {sender}\n\nBody:\n{body[:2000]}"},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("tasks", [])
    except Exception as e:
        print(f"AI task extraction error: {e}")
        return _mock_extract_tasks(subject, body, sender)


def generate_suggestions(subject: str, body: str, sender: str, intent: str) -> List[Dict]:
    """
    Generate smart suggestions (reply draft, calendar event, task creation).
    Returns: [{suggestion_type, title, content}]
    """
    if not _is_ai_available():
        return _mock_suggestions(subject, body, sender, intent)

    client = _get_client()

    system_prompt = """You are an AI email assistant. Based on the email, generate helpful suggestions.

Generate up to 3 suggestions. Each suggestion should be one of:
- "reply_draft": A professional reply draft the user can send
- "calendar_event": A calendar event to create (include title, date/time, attendees, agenda)
- "task_creation": A task summary to add to the user's task list

Return a JSON object with key "suggestions" containing an array of objects:
- "suggestion_type": one of the types above
- "title": short title for the suggestion (max 50 chars)
- "content": the full suggestion content

Always include a reply_draft if the email seems to expect a response.
Include calendar_event if a meeting is mentioned.
Include task_creation if there are clear action items.

Respond ONLY with valid JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Subject: {subject}\nFrom: {sender}\nDetected Intent: {intent}\n\nBody:\n{body[:2000]}"},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("suggestions", [])
    except Exception as e:
        print(f"AI suggestion generation error: {e}")
        return _mock_suggestions(subject, body, sender, intent)


def generate_follow_up_message(subject: str, body: str, sender: str) -> str:
    """Generate a follow-up message for an unanswered email."""
    if not _is_ai_available():
        return _mock_follow_up(subject, sender)

    client = _get_client()

    system_prompt = """You are an AI assistant. Write a polite, professional follow-up message for an email that hasn't been replied to.
Keep it concise (3-5 sentences). Acknowledge the delay and express continued interest.
Return a JSON object with key "message" containing the follow-up text.
Respond ONLY with valid JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original Subject: {subject}\nFrom: {sender}\n\nOriginal Body:\n{body[:1500]}"},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("message", "")
    except Exception as e:
        print(f"AI follow-up generation error: {e}")
        return _mock_follow_up(subject, sender)


# ──────────────── Mock / Fallback Functions ────────────────

def _mock_classify(subject: str, body: str) -> Dict:
    """Simple keyword-based classification fallback."""
    text = (subject + " " + body).lower()

    if any(w in text for w in ["newsletter", "unsubscribe", "digest", "weekly", "update"]):
        return {"classification": "informational", "intent": "general", "priority": "low"}
    if any(w in text for w in ["meeting", "schedule", "calendar", "call", "attend"]):
        return {"classification": "actionable", "intent": "schedule_meeting", "priority": "high"}
    if any(w in text for w in ["send", "document", "download", "attachment", "file", "review"]):
        return {"classification": "actionable", "intent": "send_document", "priority": "medium"}
    if any(w in text for w in ["follow up", "follow-up", "following up", "check in"]):
        return {"classification": "actionable", "intent": "follow_up_needed", "priority": "high"}
    if any(w in text for w in ["please", "confirm", "reply", "respond", "let me know", "urgent"]):
        return {"classification": "actionable", "intent": "reply_required", "priority": "high"}

    return {"classification": "informational", "intent": "general", "priority": "low"}


def _mock_extract_tasks(subject: str, body: str, sender: str) -> List[Dict]:
    """Simple task extraction fallback."""
    tasks = []
    text = (subject + " " + body).lower()

    if any(w in text for w in ["meeting", "schedule", "call"]):
        tasks.append({
            "task_type": "Schedule Meeting",
            "description": f"Schedule/confirm meeting mentioned in: {subject[:80]}",
            "deadline": "This week",
            "people_involved": sender,
            "priority": "high",
        })
    if any(w in text for w in ["review", "send", "document", "file"]):
        tasks.append({
            "task_type": "Review/Send Document",
            "description": f"Review or send document related to: {subject[:80]}",
            "deadline": "Not specified",
            "people_involved": sender,
            "priority": "medium",
        })
    if any(w in text for w in ["reply", "confirm", "respond", "let me know"]):
        tasks.append({
            "task_type": "Reply",
            "description": f"Reply to email: {subject[:80]}",
            "deadline": "ASAP",
            "people_involved": sender,
            "priority": "high",
        })

    return tasks


def _mock_suggestions(subject: str, body: str, sender: str, intent: str) -> List[Dict]:
    """Generate mock suggestions based on intent."""
    suggestions = []

    suggestions.append({
        "suggestion_type": "reply_draft",
        "title": "Draft Reply",
        "content": f"Hi,\n\nThank you for your email regarding \"{subject}\". I've noted the details and will follow up shortly.\n\nBest regards",
    })

    if intent in ("schedule_meeting",):
        suggestions.append({
            "suggestion_type": "calendar_event",
            "title": "Create Calendar Event",
            "content": f"📅 {subject}\n👥 {sender}\n📝 Details from email",
        })

    if intent in ("reply_required", "send_document", "follow_up_needed"):
        suggestions.append({
            "suggestion_type": "task_creation",
            "title": "Create Task",
            "content": f"📋 Action required for: {subject}\n👤 From: {sender}\n⚡ Priority: Based on email urgency",
        })

    return suggestions


def _mock_follow_up(subject: str, sender: str) -> str:
    """Generate a mock follow-up message."""
    return (
        f"Hi,\n\n"
        f"I wanted to follow up on your email regarding \"{subject}\". "
        f"I apologize for the delayed response. I'm still very interested and would love to continue our conversation.\n\n"
        f"Could you let me know a good time to connect?\n\n"
        f"Best regards"
    )
