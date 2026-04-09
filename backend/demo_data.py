"""
Demo data — realistic sample emails with pre-computed AI classifications.
Used when DEMO_MODE=true to showcase the full UI without API keys.
"""
import random
from datetime import datetime, timezone, timedelta

NOW = datetime.now(timezone.utc)

# ─── HIGH QUALITY MANUAL EMAILS (1-16) ─────────────────────────────────────────

_MANUAL_EMAILS = [
    {
        "gmail_id": "demo_001",
        "sender": "sarah.chen@techcorp.io",
        "sender_name": "Sarah Chen",
        "subject": "Q2 Budget Review Meeting — Please Confirm Attendance",
        "body": "Hi,\n\nI'd like to schedule a Q2 budget review meeting for next Wednesday at 2:00 PM. We'll be covering marketing spend, engineering headcount, and product launch timeline.\n\nPlease confirm your attendance and bring the latest revenue forecasts.",
        "snippet": "I'd like to schedule a Q2 budget review meeting for next Wednesday...",
        "received_at": NOW - timedelta(minutes=15),
        "is_read": False,
        "classification": "actionable",
        "intent": "schedule_meeting",
        "priority": "high",
    },
    {
        "gmail_id": "demo_002",
        "sender": "james.wilson@clienthub.com",
        "sender_name": "James Wilson",
        "subject": "RE: Proposal Draft — Needs Revisions Before Friday",
        "body": "Hello,\n\nI've reviewed the proposal. We need to update pricing for volume discounts, extend the timeline by 2 weeks, and add SLA commitments.\n\nRevised version needed by Friday EOD.",
        "snippet": "I've reviewed the proposal draft and we have a few important revisions...",
        "received_at": NOW - timedelta(hours=1),
        "is_read": False,
        "classification": "actionable",
        "intent": "reply_required",
        "priority": "high",
    },
    {
        "gmail_id": "demo_003",
        "sender": "newsletter@techdigest.io",
        "sender_name": "Tech Digest Weekly",
        "subject": "🚀 This Week in AI: OpenAI Launches GPT-5, Google Responds",
        "body": "TOP STORIES: OpenAI launches GPT-5, Google announces Gemini 2.0, Meta releases new open-source LLM.",
        "snippet": "This Week in AI: OpenAI Launches GPT-5, Google Responds...",
        "received_at": NOW - timedelta(hours=2),
        "is_read": True,
        "classification": "informational",
        "intent": "general",
        "priority": "low",
    },
    {
        "gmail_id": "demo_004",
        "sender": "priya.sharma@designlab.co",
        "sender_name": "Priya Sharma",
        "subject": "Updated Brand Guidelines — Please Review & Download",
        "body": "The updated brand guidelines are ready: Brand Guidelines v3.2. Includes new color palette and icon library. Please review by end of week.",
        "snippet": "The updated brand guidelines are ready! Please review and download...",
        "received_at": NOW - timedelta(hours=3),
        "is_read": False,
        "classification": "actionable",
        "intent": "send_document",
        "priority": "medium",
    },
    {
        "gmail_id": "demo_005",
        "sender": "alex.rivera@startupxyz.com",
        "sender_name": "Alex Rivera",
        "subject": "Follow-up: Partnership Discussion from Last Week",
        "body": "I've put together a preliminary integration roadmap. Available for a 30-min call this week? Also, please share the API documentation.",
        "snippet": "I wanted to follow up on our conversation about the partnership...",
        "received_at": NOW - timedelta(hours=5),
        "is_read": True,
        "classification": "actionable",
        "intent": "follow_up_needed",
        "priority": "high",
    },
    {
        "gmail_id": "demo_006",
        "sender": "hr@company.com",
        "sender_name": "HR Department",
        "subject": "Reminder: Annual Performance Reviews Due April 15",
        "body": "Performance reviews are due April 15th. Complete self-assessment and schedule 1-on-1 with manager.",
        "snippet": "Annual performance reviews are due by April 15th...",
        "received_at": NOW - timedelta(hours=8),
        "is_read": True,
        "classification": "actionable",
        "intent": "reply_required",
        "priority": "medium",
    },
    {
        "gmail_id": "demo_007",
        "sender": "security@github.com",
        "sender_name": "GitHub Security",
        "subject": "[GitHub] Dependabot Alert: Critical vulnerability in lodash",
        "body": "A critical vulnerability (CVE-2026-1234) has been found in lodash. Severity: Critical. PR #456 opened to fix.",
        "snippet": "Critical vulnerability found in lodash < 4.17.22 in your repository...",
        "received_at": NOW - timedelta(hours=14),
        "is_read": False,
        "classification": "actionable",
        "intent": "reply_required",
        "priority": "high",
    },
    {
        "gmail_id": "demo_008",
        "sender": "events@meetup.com",
        "sender_name": "Meetup Events",
        "subject": "You're invited: AI & Machine Learning Meetup — April 20",
        "body": "Join us for talks and networking on April 20. Speakers: Dr. Emily Zhang, Mark Thompson.",
        "snippet": "Join us for an AI & Machine Learning Meetup on April 20...",
        "received_at": NOW - timedelta(hours=20),
        "is_read": True,
        "classification": "informational",
        "intent": "schedule_meeting",
        "priority": "low",
    },
    {
        "gmail_id": "demo_009",
        "sender": "support@cloudhost.net",
        "sender_name": "CloudHost Support",
        "subject": "[Ticket #8821] Potential Service Interruption Alert",
        "body": "Unusual traffic patterns on US-East-1. Scaling actions taken. Review dashboard immediately.",
        "snippet": "Unusual traffic patterns detected on your production cluster...",
        "received_at": NOW - timedelta(hours=2),
        "is_read": False,
        "classification": "actionable",
        "intent": "reply_required",
        "priority": "high",
    },
    {
        "gmail_id": "demo_010",
        "sender": "legal@legalservices.com",
        "sender_name": "Legal Services Team",
        "subject": "Urgent: MSA Agreement for New Client — Review Required",
        "body": "Client redlined Liability/Indemnification clauses. Approval needed by tomorrow morning.",
        "snippet": "Attached is the MSA for the new client with significant redlines...",
        "received_at": NOW - timedelta(hours=4),
        "is_read": False,
        "classification": "actionable",
        "intent": "send_document",
        "priority": "high",
    },
    {
        "gmail_id": "demo_011",
        "sender": "no-reply@delta.com",
        "sender_name": "Delta Air Lines",
        "subject": "Flight Confirmation - DL1234 - Seattle to San Francisco",
        "body": "Confirmation: GHK789. Departure: SEA 10:30 AM. Arrival: SFO 1:00 PM.",
        "snippet": "Flight Confirmation DL1234 from Seattle to San Francisco...",
        "received_at": NOW - timedelta(hours=10),
        "is_read": True,
        "classification": "informational",
        "intent": "general",
        "priority": "low",
    },
    {
        "gmail_id": "demo_012",
        "sender": "shipping@amazon.com",
        "sender_name": "Amazon Shipping",
        "subject": "Your package has been delivered!",
        "body": "Package delivered at 2:15 PM. Items: UltraWide Monitor, Ergonomic Keyboard.",
        "snippet": "Your package containing UltraWide Monitor was delivered...",
        "received_at": NOW - timedelta(hours=14),
        "is_read": True,
        "classification": "informational",
        "intent": "general",
        "priority": "low",
    },
    {
        "gmail_id": "demo_013",
        "sender": "karen.recruiter@talentforce.com",
        "sender_name": "Karen Recruiter",
        "subject": "Interview Request: Senior AI Engineer Candidate",
        "body": "David Kovacs (8y exp NLP/RAG). Available Friday 10 AM - 12 PM for technical interview.",
        "snippet": "Interview request for Senior AI Engineer candidate David Kovacs...",
        "received_at": NOW - timedelta(hours=20),
        "is_read": False,
        "classification": "actionable",
        "intent": "schedule_meeting",
        "priority": "medium",
    },
    {
        "gmail_id": "demo_014",
        "sender": "michael.scott@dundermifflin.com",
        "sender_name": "Michael Scott",
        "subject": "Quick Coffee?",
        "body": "Hey, free for coffee this afternoon? I have a big idea for sales strategy.",
        "snippet": "Are you free for a coffee this afternoon? I have a big idea...",
        "received_at": NOW - timedelta(hours=22),
        "is_read": False,
        "classification": "actionable",
        "intent": "schedule_meeting",
        "priority": "low",
    },
    {
        "gmail_id": "demo_015",
        "sender": "ryan.howard@corp.com",
        "sender_name": "Ryan Howard",
        "subject": "Project WUPHF Update",
        "body": "Mobile integration 90% complete. Beta launch Monday. No action needed.",
        "snippet": "Update on Project WUPHF: Mobile integration 90% complete...",
        "received_at": NOW - timedelta(hours=36),
        "is_read": True,
        "classification": "informational",
        "intent": "general",
        "priority": "low",
    },
    {
        "gmail_id": "demo_016",
        "sender": "monitor@uptime-robot.io",
        "sender_name": "UptimeRobot",
        "subject": "ALERT: Master Database Server is DOWN",
        "body": "Monitor Master DB (Primary) is DOWN since 5:42 AM. Connection timed out. Investigation required.",
        "snippet": "CRITICAL: Master Database Server is currently DOWN since 5:42 AM...",
        "received_at": NOW - timedelta(hours=1),
        "is_read": False,
        "classification": "actionable",
        "intent": "reply_required",
        "priority": "high",
    },
]

# ─── BULK GENERATOR (17-60) ───────────────────────────────────────────────────

def _generate_bulk_data():
    emails = []
    tasks = []
    suggestions = []
    
    # Newsletter Templates
    newsletters = [
        ("Medium Daily", "The 10 Best Productivity Hacks for AI Engineers"),
        ("Hacker News", "Show HN: A new framework for distributed state"),
        ("Wall Street Journal", "Market Morning: Tech Stocks Rally on Earnings"),
        ("The Verge", "Apple's New VR Headset: First Impressions"),
        ("Product Hunt", "Daily Top 10: New AI Tools to Boost Your Workflow"),
    ]
    
    # System Templates
    systems = [
        ("Jira", "[DEVOPS-442] Ticket assigned to you: Fix login latency"),
        ("Slack", "You have 3 unread messages in #general"),
        ("Jenkins", "Build #1242 for 'production-deploy' SUCCESS"),
        ("Zoom", "Meeting Recording is now available (Q1 Sync)"),
        ("Google Calendar", "Reminder: Standup in 10 minutes"),
    ]
    
    # Standard Work Templates
    work = [
        ("Tom Barker", "Review requested on PR #221: Fix auth bug"),
        ("Project Tracker", "Next week's timeline finalized"),
        ("Accounts", "Invoice #8821 for Cloud Services is ready"),
        ("IT Support", "Password expiry reminder: 5 days left"),
        ("Marketing", "Final assets for the social campaign"),
    ]

    # Generate 45 more emails (Total 61)
    for i in range(45):
        idx = i + 16 # Start after manual ones
        category = random.choice(["news", "sys", "work"])
        
        if category == "news":
            name, sub = random.choice( newsleters if 'newsleters' in locals() else newsletters )
            is_action = False
            intent = "general"
            priority = "low"
            body = f"Welcome to today's edition of {name}. Featured story: {sub}. Read more at our website."
        elif category == "sys":
            name, sub = random.choice( systems )
            is_action = True if "Ticket" in sub or "Reminder" in sub else False
            intent = "reply_required" if is_action else "general"
            priority = "medium"
            body = f"Notification from {name}: {sub}. Visit your dashboard for more details."
        else:
            name, sub = random.choice( work )
            is_action = True
            intent = "reply_required" if "Review" in sub else "general"
            priority = "medium"
            body = f"Hi, regarding {sub}... please take a look when you have a moment. Thanks, {name.split()[0]}."

        received_at = NOW - timedelta(days=random.randint(2, 7), hours=random.randint(0, 23))
        
        email_id = f"demo_{idx+1:03d}"
        emails.append({
            "gmail_id": email_id,
            "sender": f"{name.lower().replace(' ', '.')}@demo.com",
            "sender_name": name,
            "subject": sub,
            "body": body,
            "snippet": body[:100] + "...",
            "received_at": received_at,
            "is_read": True if random.random() > 0.4 else False,
            "classification": "actionable" if is_action else "informational",
            "intent": intent,
            "priority": priority,
        })
        
        if is_action:
            tasks.append({
                "email_index": idx,
                "task_type": "Review" if "Review" in sub else "Action Item",
                "description": f"Process update from {name}: {sub}",
                "deadline": "Next week",
                "people_involved": name,
                "priority": priority,
                "status": "todo",
            })
            suggestions.append({
                "email_index": idx,
                "suggestion_type": "reply_draft",
                "title": "Acknowledge Update",
                "content": f"Hi {name.split()[0]},\n\nThanks for the update on '{sub}'. I'll take a look and get back to you shortly.\n\nBest regards"
            })

    return emails, tasks, suggestions

_BULK_EMAILS, _BULK_TASKS, _BULK_SUGGESTIONS = _generate_bulk_data()

# ─── FINAL EXPORTED LISTS ──────────────────────────────────────────────────────

DEMO_EMAILS = _MANUAL_EMAILS + _BULK_EMAILS

DEMO_TASKS = [
    {
        "email_index": 0,
        "task_type": "Schedule Meeting",
        "description": "Confirm attendance for Q2 budget review meeting — Wednesday 2:00 PM",
        "deadline": "Next Wednesday",
        "people_involved": "Sarah Chen",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 0,
        "task_type": "Prepare Document",
        "description": "Prepare latest revenue forecasts for the budget review meeting",
        "deadline": "Next Wednesday",
        "people_involved": "Sarah Chen",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 1,
        "task_type": "Revise Document",
        "description": "Update proposal pricing section with new volume discounts",
        "deadline": "Friday EOD",
        "people_involved": "James Wilson",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 1,
        "task_type": "Revise Document",
        "description": "Extend timeline in Section 3 by two weeks for QA phase",
        "deadline": "Friday EOD",
        "people_involved": "James Wilson",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 3,
        "task_type": "Review Document",
        "description": "Review updated brand guidelines v3.2 and provide feedback",
        "deadline": "End of week",
        "people_involved": "Priya Sharma",
        "priority": "medium",
        "status": "todo",
    },
    {
        "email_index": 4,
        "task_type": "Schedule Meeting",
        "description": "Schedule 30-min call with Alex Rivera",
        "deadline": "This week",
        "people_involved": "Alex Rivera",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 6,
        "task_type": "Fix Issue",
        "description": "Merge Dependabot PR #456 for lodash fix",
        "deadline": "ASAP",
        "people_involved": "Engineering Team",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 8,
        "task_type": "Check Infrastructure",
        "description": "Review scaling actions on production cluster",
        "deadline": "Today",
        "people_involved": "DevOps",
        "priority": "high",
        "status": "todo",
    },
    {
        "email_index": 15,
        "task_type": "Incident Response",
        "description": "Restore Master DB",
        "deadline": "IMMEDIATE",
        "people_involved": "SRE",
        "priority": "high",
        "status": "todo",
    },
] + _BULK_TASKS

DEMO_SUGGESTIONS = [
    {
        "email_index": 0,
        "suggestion_type": "reply_draft",
        "title": "Confirm Meeting",
        "content": "Hi Sarah, I'd like to confirm my attendance for next Wednesday. Best regards"
    },
    {
        "email_index": 1,
        "suggestion_type": "reply_draft",
        "title": "Acknowledge Revisions",
        "content": "Hi James, I've noted all three points. Revised proposal by Friday. Best regards"
    },
    {
        "email_index": 6,
        "suggestion_type": "task_creation",
        "title": "Security Fix",
        "content": "🚨 Immediate action: Merge PR #456 for lodash vulnerability fix."
    },
] + _BULK_SUGGESTIONS

DEMO_FOLLOWUPS = [
    {
        "email_index": 4,  # Alex Rivera
        "suggested_message": "Hi Alex,\n\nI wanted to follow up on your message about the partnership discussion. Apologies for the delay.\n\nBest regards",
        "reason": "Partnership follow-up email received 12+ hours ago with no reply sent",
        "hours_elapsed": 12,
    },
    {
        "email_index": 8, # CloudHost
        "suggested_message": "Team,\n\nConfirmed the scaling actions for Ticket #8821. No further issues detected.\n\nBest regards",
        "reason": "Infrastructure alert received 2+ hours ago — urgent status",
        "hours_elapsed": 2,
    },
]
