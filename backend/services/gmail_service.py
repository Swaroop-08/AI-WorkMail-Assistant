"""
Gmail API Service — fetches and parses emails from the user's Gmail inbox.
Falls back to demo data when DEMO_MODE is enabled.
"""
import os
import sys
import base64
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional
from email.utils import parsedate_to_datetime

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

# Resolve credentials path to absolute path at module load
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_THIS_DIR)
_PROJECT_DIR = os.path.dirname(_BACKEND_DIR)

# Look for credentials in multiple locations
_CREDS_CANDIDATES = [
    os.getenv("GMAIL_CREDENTIALS_PATH", ""),
    os.path.join(_PROJECT_DIR, "client_secret_630244622777-9ddmbpff2ptkjklhbk7nveq899l3s2sp.apps.googleusercontent.com.json"),
    os.path.join(_BACKEND_DIR, "client_secret_630244622777-9ddmbpff2ptkjklhbk7nveq899l3s2sp.apps.googleusercontent.com.json"),
    os.path.join(_BACKEND_DIR, "credentials.json"),
]


def _find_credentials() -> str:
    """Find the Gmail credentials JSON file."""
    for path in _CREDS_CANDIDATES:
        if path and os.path.isabs(path) and os.path.exists(path):
            return path
        elif path and not os.path.isabs(path):
            # Try relative to backend dir
            abs_path = os.path.join(_BACKEND_DIR, path)
            if os.path.exists(abs_path):
                return abs_path
            # Try relative to project dir
            abs_path = os.path.join(_PROJECT_DIR, path)
            if os.path.exists(abs_path):
                return abs_path
    return ""


def _get_gmail_service():
    """Build and return an authenticated Gmail API service object."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    token_path = os.path.join(_BACKEND_DIR, "token.json")
    creds_path = _find_credentials()

    print(f"[GMAIL] Token path: {token_path}")
    print(f"[GMAIL] Credentials path: {creds_path}")
    print(f"[GMAIL] Credentials exists: {os.path.exists(creds_path) if creds_path else False}")

    if os.path.exists(token_path):
        print("[GMAIL] Loading existing token...")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[GMAIL] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not creds_path or not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"Gmail credentials file not found! Searched:\n"
                    + "\n".join(f"  - {p}" for p in _CREDS_CANDIDATES if p)
                    + "\nPlease place your credentials.json in the backend/ or project root directory."
                )
            print(f"[GMAIL] Starting OAuth flow... A browser window should open.")
            print(f"[GMAIL] If the browser doesn't open, check the URL printed below:")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=8090, open_browser=True)
            print("[GMAIL] OAuth flow completed successfully!")

        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
            print(f"[GMAIL] Token saved to {token_path}")

    service = build("gmail", "v1", credentials=creds)
    print("[GMAIL] Gmail service built successfully!")
    return service


def _extract_body(payload: dict) -> str:
    """Recursively extract the plain text body from a Gmail message payload."""
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
                    break
            elif mime_type.startswith("multipart/"):
                body = _extract_body(part)
                if body:
                    break
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    return body.strip()


def _parse_sender(sender_str: str) -> tuple:
    """Parse 'Name <email>' format into (name, email)."""
    match = re.match(r'^"?([^"<]*)"?\s*<?([^>]*)>?$', sender_str.strip())
    if match:
        name = match.group(1).strip().strip('"')
        email = match.group(2).strip()
        return (name if name else email, email)
    return (sender_str, sender_str)


def fetch_latest_emails(max_results: int = 20) -> List[Dict]:
    """
    Fetch the latest emails from Gmail inbox.
    Returns a list of parsed email dicts.
    """
    print(f"[GMAIL] fetch_latest_emails called. DEMO_MODE={DEMO_MODE}")

    if DEMO_MODE:
        print("[GMAIL] Using demo data...")
        from demo_data import DEMO_EMAILS
        return DEMO_EMAILS

    print("[GMAIL] Connecting to Gmail API...")
    service = _get_gmail_service()

    print("[GMAIL] Fetching message list...")
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        labelIds=["INBOX"],
    ).execute()

    messages = results.get("messages", [])
    print(f"[GMAIL] Found {len(messages)} messages")
    emails = []

    for msg_info in messages:
        try:
            msg = service.users().messages().get(
                userId="me",
                id=msg_info["id"],
                format="full",
            ).execute()

            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            sender_raw = headers.get("From", "Unknown")
            sender_name, sender_email = _parse_sender(sender_raw)

            # Parse date
            date_str = headers.get("Date", "")
            try:
                received_at = parsedate_to_datetime(date_str)
                if received_at.tzinfo is None:
                    received_at = received_at.replace(tzinfo=timezone.utc)
            except Exception:
                received_at = datetime.now(timezone.utc)

            body = _extract_body(msg.get("payload", {}))
            snippet = msg.get("snippet", "")

            emails.append({
                "gmail_id": msg["id"],
                "sender": sender_email,
                "sender_name": sender_name,
                "subject": headers.get("Subject", "(No Subject)"),
                "body": body if body else snippet,
                "snippet": snippet[:200],
                "received_at": received_at,
                "is_read": "UNREAD" not in msg.get("labelIds", []),
                "classification": "",
                "intent": "",
                "priority": "medium",
            })
        except Exception as e:
            print(f"[GMAIL] Error parsing message {msg_info['id']}: {e}")
            continue

    print(f"[GMAIL] Successfully parsed {len(emails)} emails")
    return emails
