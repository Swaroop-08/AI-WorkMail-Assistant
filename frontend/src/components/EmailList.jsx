import { useState, useEffect } from 'react';
import StatusBadge from './StatusBadge';

const AVATAR_COLORS = [
  '#7c3aed', '#4f46e5', '#06b6d4', '#10b981',
  '#f59e0b', '#f43f5e', '#f97316', '#8b5cf6',
  '#ec4899', '#14b8a6', '#6366f1', '#d946ef',
];

function getAvatarColor(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length];
}

function getInitials(name) {
  if (!name) return '?';
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
}

function timeAgo(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export default function EmailList({
  emails,
  selectedId,
  onSelect,
  loading,
}) {
  const [filter, setFilter] = useState('all');

  const filteredEmails = emails.filter((email) => {
    if (filter === 'all') return true;
    if (filter === 'actionable') return email.classification === 'actionable';
    if (filter === 'informational') return email.classification === 'informational';
    if (filter === 'unread') return !email.is_read;
    return true;
  });

  const filters = [
    { id: 'all', label: 'All' },
    { id: 'actionable', label: '⚡ Actionable' },
    { id: 'informational', label: 'ℹ️ Info' },
    { id: 'unread', label: '● Unread' },
  ];

  return (
    <div className="email-list-panel">
      <div className="email-list-header">
        <span className="email-list-title">Inbox</span>
        <span className="email-list-count">{emails.length} emails</span>
      </div>

      <div className="email-list-filters">
        {filters.map((f) => (
          <button
            key={f.id}
            className={`filter-chip ${filter === f.id ? 'active' : ''}`}
            onClick={() => setFilter(f.id)}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="email-list-scroll">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <span className="loading-text">Loading emails...</span>
          </div>
        ) : filteredEmails.length === 0 ? (
          <div className="empty-state">
            <span className="empty-state-icon">📭</span>
            <span className="empty-state-title">No emails</span>
            <span className="empty-state-text">
              Click "Fetch Emails" to load your inbox
            </span>
          </div>
        ) : (
          filteredEmails.map((email) => (
            <div
              key={email.id}
              className={`email-item ${selectedId === email.id ? 'active' : ''} ${!email.is_read ? 'unread' : ''}`}
              onClick={() => onSelect(email.id)}
              id={`email-item-${email.id}`}
            >
              <div
                className="email-avatar"
                style={{ backgroundColor: getAvatarColor(email.sender_name || email.sender) }}
              >
                {getInitials(email.sender_name || email.sender)}
              </div>
              <div className="email-item-content">
                <div className="email-item-top">
                  <span className="email-item-sender">
                    {email.sender_name || email.sender}
                  </span>
                  <span className="email-item-time">
                    {timeAgo(email.received_at)}
                  </span>
                </div>
                <div className="email-item-subject">{email.subject}</div>
                <div className="email-item-snippet">{email.snippet}</div>
                <div className="email-item-badges">
                  {email.classification && (
                    <StatusBadge type="classification" value={email.classification} />
                  )}
                  {email.intent && email.intent !== 'general' && (
                    <StatusBadge type="intent" value={email.intent} />
                  )}
                  {email.priority === 'high' && (
                    <StatusBadge type="priority" value="high" />
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
