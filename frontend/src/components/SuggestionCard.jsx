import { useState } from 'react';

const ICONS = {
  reply_draft: '💬',
  calendar_event: '📅',
  task_creation: '✅',
  follow_up: '🔄',
};

const LABELS = {
  reply_draft: 'Reply Draft',
  calendar_event: 'Calendar Event',
  task_creation: 'Task Creation',
  follow_up: 'Follow-Up',
};

export default function SuggestionCard({ suggestion, onApprove, onDismiss }) {
  const [actionLoading, setActionLoading] = useState(null);

  const handleApprove = async () => {
    setActionLoading('approve');
    try {
      await onApprove(suggestion.id);
    } finally {
      setActionLoading(null);
    }
  };

  const handleDismiss = async () => {
    setActionLoading('dismiss');
    try {
      await onDismiss(suggestion.id);
    } finally {
      setActionLoading(null);
    }
  };

  const isPending = suggestion.status === 'pending';

  return (
    <div className={`suggestion-card ${suggestion.suggestion_type} ${suggestion.status} animate-fade-in-up`}>
      <div className="suggestion-header">
        <div className={`suggestion-type-icon ${suggestion.suggestion_type}`}>
          {ICONS[suggestion.suggestion_type] || '💡'}
        </div>
        <span className="suggestion-title">{suggestion.title}</span>
        <div className="suggestion-status-badge">
          <span className={`badge badge-${suggestion.status}`}>
            {suggestion.status === 'approved' ? '✅ Approved' :
             suggestion.status === 'dismissed' ? '✖ Dismissed' :
             `${LABELS[suggestion.suggestion_type] || 'Suggestion'}`}
          </span>
        </div>
      </div>

      <div className="suggestion-content">
        {suggestion.content}
      </div>

      {isPending && (
        <div className="suggestion-actions">
          <button
            className="btn btn-danger btn-sm"
            onClick={handleDismiss}
            disabled={actionLoading !== null}
          >
            {actionLoading === 'dismiss' ? '...' : '✕ Dismiss'}
          </button>
          <button
            className="btn btn-success btn-sm"
            onClick={handleApprove}
            disabled={actionLoading !== null}
          >
            {actionLoading === 'approve' ? '...' : '✓ Approve'}
          </button>
        </div>
      )}
    </div>
  );
}
