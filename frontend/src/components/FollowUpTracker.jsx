import { useState, useEffect } from 'react';
import { getFollowUps, scanFollowUps, approveFollowUp, dismissFollowUp } from '../api';
import LoadingSpinner from './LoadingSpinner';

export default function FollowUpTracker() {
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);

  const loadFollowUps = async () => {
    setLoading(true);
    try {
      const data = await getFollowUps();
      setFollowUps(data);
    } catch (err) {
      console.error('Failed to load follow-ups:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFollowUps();
  }, []);

  const handleScan = async () => {
    setScanning(true);
    try {
      await scanFollowUps();
      await loadFollowUps();
    } catch (err) {
      console.error('Scan failed:', err);
    } finally {
      setScanning(false);
    }
  };

  const handleApprove = async (id) => {
    try {
      await approveFollowUp(id);
      setFollowUps((prev) =>
        prev.map((fu) => (fu.id === id ? { ...fu, status: 'approved' } : fu))
      );
    } catch (err) {
      console.error('Approve failed:', err);
    }
  };

  const handleDismiss = async (id) => {
    try {
      await dismissFollowUp(id);
      setFollowUps((prev) =>
        prev.map((fu) => (fu.id === id ? { ...fu, status: 'dismissed' } : fu))
      );
    } catch (err) {
      console.error('Dismiss failed:', err);
    }
  };

  const pendingCount = followUps.filter((fu) => fu.status === 'pending').length;

  if (loading) {
    return <LoadingSpinner text="Loading follow-ups..." />;
  }

  return (
    <div className="followup-tracker">
      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card amber">
          <div className="stat-icon amber">🔔</div>
          <div className="stat-info">
            <div className="stat-value">{followUps.length}</div>
            <div className="stat-label">Total Follow-Ups</div>
          </div>
        </div>
        <div className="stat-card rose">
          <div className="stat-icon rose">⏳</div>
          <div className="stat-info">
            <div className="stat-value">{pendingCount}</div>
            <div className="stat-label">Pending Action</div>
          </div>
        </div>
        <div className="stat-card emerald">
          <div className="stat-icon emerald">✅</div>
          <div className="stat-info">
            <div className="stat-value">
              {followUps.filter((fu) => fu.status === 'approved').length}
            </div>
            <div className="stat-label">Approved</div>
          </div>
        </div>
        <div className="stat-card violet">
          <div className="stat-icon violet">🔍</div>
          <div className="stat-info">
            <div style={{ marginTop: '4px' }}>
              <button
                className={`btn btn-primary btn-sm ${scanning ? 'btn-loading' : ''}`}
                onClick={handleScan}
                disabled={scanning}
                id="btn-scan-followups"
              >
                {scanning ? '⟳ Scanning...' : '🔍 Scan Now'}
              </button>
            </div>
            <div className="stat-label" style={{ marginTop: '4px' }}>Detect Stale Emails</div>
          </div>
        </div>
      </div>

      {/* Follow-Up List */}
      {followUps.length === 0 ? (
        <div className="empty-state">
          <span className="empty-state-icon">🔔</span>
          <span className="empty-state-title">No follow-ups detected</span>
          <span className="empty-state-text">
            Click "Scan Now" to check for emails that need follow-up
          </span>
        </div>
      ) : (
        <div className="followup-list stagger-children">
          {followUps.map((fu) => (
            <div
              key={fu.id}
              className={`followup-card ${fu.status} animate-fade-in-up`}
              id={`followup-${fu.id}`}
            >
              <div className="followup-header">
                <div className="followup-email-info">
                  <div className="followup-subject">{fu.email_subject}</div>
                  <div className="followup-sender">From: {fu.email_sender}</div>
                </div>
                <div className="followup-time-badge">
                  ⏰ {fu.hours_elapsed}h elapsed
                </div>
              </div>

              <div className="followup-reason">{fu.reason}</div>

              <div style={{ marginBottom: '12px' }}>
                <span
                  className="classification-label"
                  style={{ display: 'block', marginBottom: '8px' }}
                >
                  Suggested Follow-Up Message:
                </span>
                <div className="followup-message">{fu.suggested_message}</div>
              </div>

              {fu.status === 'pending' ? (
                <div className="followup-actions">
                  <button
                    className="btn btn-danger btn-sm"
                    onClick={() => handleDismiss(fu.id)}
                  >
                    ✕ Dismiss
                  </button>
                  <button
                    className="btn btn-success btn-sm"
                    onClick={() => handleApprove(fu.id)}
                  >
                    ✓ Approve Follow-Up
                  </button>
                </div>
              ) : (
                <div className="followup-actions">
                  <span className={`badge badge-${fu.status}`}>
                    {fu.status === 'approved' ? '✅ Approved' : '✖ Dismissed'}
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
