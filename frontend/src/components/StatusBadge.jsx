export default function StatusBadge({ type, value }) {
  if (!value) return null;

  const labels = {
    // Classification
    actionable: '⚡ Actionable',
    informational: 'ℹ️ Informational',
    // Intent
    reply_required: '💬 Reply Required',
    schedule_meeting: '📅 Schedule Meeting',
    send_document: '📄 Send Document',
    follow_up_needed: '🔄 Follow-up Needed',
    general: '📌 General',
    // Priority
    high: '🔴 High',
    medium: '🟡 Medium',
    low: '🟢 Low',
    // Status
    todo: '📋 To Do',
    in_progress: '🔧 In Progress',
    done: '✅ Done',
    // Suggestion status
    pending: '⏳ Pending',
    approved: '✅ Approved',
    dismissed: '✖ Dismissed',
  };

  return (
    <span className={`badge badge-${value}`}>
      {labels[value] || value}
    </span>
  );
}
