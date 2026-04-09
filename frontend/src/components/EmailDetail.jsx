import { useState, useEffect } from 'react';
import { getEmailDetail, approveSuggestion, dismissSuggestion } from '../api';
import StatusBadge from './StatusBadge';
import SuggestionCard from './SuggestionCard';
import LoadingSpinner from './LoadingSpinner';

function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function EmailDetail({ emailId, onUpdate }) {
  const [email, setEmail] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (emailId) {
      setLoading(true);
      getEmailDetail(emailId)
        .then((data) => setEmail(data))
        .catch(() => setEmail(null))
        .finally(() => setLoading(false));
    } else {
      setEmail(null);
    }
  }, [emailId]);

  const handleApprove = async (suggestionId) => {
    await approveSuggestion(emailId, suggestionId);
    // Update local state
    setEmail((prev) => ({
      ...prev,
      suggestions: prev.suggestions.map((s) =>
        s.id === suggestionId ? { ...s, status: 'approved' } : s
      ),
    }));
    if (onUpdate) onUpdate();
  };

  const handleDismiss = async (suggestionId) => {
    await dismissSuggestion(emailId, suggestionId);
    setEmail((prev) => ({
      ...prev,
      suggestions: prev.suggestions.map((s) =>
        s.id === suggestionId ? { ...s, status: 'dismissed' } : s
      ),
    }));
    if (onUpdate) onUpdate();
  };

  if (!emailId) {
    return (
      <div className="email-detail-panel">
        <div className="email-detail-empty">
          <span className="email-detail-empty-icon">📧</span>
          <span className="email-detail-empty-text">
            Select an email to view details and AI suggestions
          </span>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="email-detail-panel">
        <LoadingSpinner text="Loading email..." />
      </div>
    );
  }

  if (!email) {
    return (
      <div className="email-detail-panel">
        <div className="email-detail-empty">
          <span className="email-detail-empty-icon">❌</span>
          <span className="email-detail-empty-text">Email not found</span>
        </div>
      </div>
    );
  }

  const pendingSuggestions = email.suggestions?.filter((s) => s.status === 'pending') || [];
  const otherSuggestions = email.suggestions?.filter((s) => s.status !== 'pending') || [];

  return (
    <div className="email-detail-panel">
      <div className="email-detail animate-fade-in">
        {/* Header */}
        <div className="email-detail-header">
          <h2 className="email-detail-subject">{email.subject}</h2>
          <div className="email-detail-meta">
            <div className="email-detail-sender-info">
              <div>
                <div className="email-detail-sender-name">
                  {email.sender_name || email.sender}
                </div>
                {email.sender_name && (
                  <div className="email-detail-sender-email">{email.sender}</div>
                )}
              </div>
            </div>
            <span className="email-detail-time">{formatDate(email.received_at)}</span>
          </div>
        </div>

        {/* Classification Banner */}
        <div className="email-detail-classification">
          <span className="classification-label">AI Analysis:</span>
          <StatusBadge type="classification" value={email.classification} />
          <StatusBadge type="intent" value={email.intent} />
          <StatusBadge type="priority" value={email.priority} />
        </div>

        {/* Body */}
        <div className="email-detail-body">{email.body}</div>

        {/* Tasks */}
        {email.tasks && email.tasks.length > 0 && (
          <div className="suggestions-section">
            <h3 className="section-title">
              <span className="section-title-icon">📋</span>
              Extracted Tasks ({email.tasks.length})
            </h3>
            <div className="suggestions-grid">
              {email.tasks.map((task) => (
                <div key={task.id} className="suggestion-card task_creation animate-fade-in-up">
                  <div className="suggestion-header">
                    <div className="suggestion-type-icon task_creation">✅</div>
                    <span className="suggestion-title">{task.task_type}</span>
                    <StatusBadge type="priority" value={task.priority} />
                  </div>
                  <div className="suggestion-content">
                    {task.description}
                    {task.deadline && `\n📅 Deadline: ${task.deadline}`}
                    {task.people_involved && `\n👥 People: ${task.people_involved}`}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI Suggestions */}
        {email.suggestions && email.suggestions.length > 0 && (
          <div className="suggestions-section">
            <h3 className="section-title">
              <span className="section-title-icon">🤖</span>
              AI Suggestions ({email.suggestions.length})
            </h3>
            <div className="suggestions-grid stagger-children">
              {pendingSuggestions.map((sug) => (
                <SuggestionCard
                  key={sug.id}
                  suggestion={sug}
                  onApprove={handleApprove}
                  onDismiss={handleDismiss}
                />
              ))}
              {otherSuggestions.map((sug) => (
                <SuggestionCard
                  key={sug.id}
                  suggestion={sug}
                  onApprove={handleApprove}
                  onDismiss={handleDismiss}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
