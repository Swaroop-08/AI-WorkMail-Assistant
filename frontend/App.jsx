import { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import EmailList from './components/EmailList';
import EmailDetail from './components/EmailDetail';
import TaskBoard from './components/TaskBoard';
import FollowUpTracker from './components/FollowUpTracker';
import { fetchEmailsFromGmail, getEmails, getStats } from './api';

const VIEW_TITLES = {
  inbox: { title: 'Inbox', subtitle: 'AI-analyzed emails with smart suggestions' },
  tasks: { title: 'Task Board', subtitle: 'Extracted tasks from your emails' },
  followups: { title: 'Follow-Up Tracker', subtitle: 'Emails that need your attention' },
};

export default function App() {
  const [activeView, setActiveView] = useState('inbox');
  const [emails, setEmails] = useState([]);
  const [selectedEmailId, setSelectedEmailId] = useState(null);
  const [stats, setStats] = useState({});
  const [fetchLoading, setFetchLoading] = useState(false);
  const [emailsLoading, setEmailsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadEmails = useCallback(async () => {
    setEmailsLoading(true);
    try {
      const data = await getEmails();
      setEmails(data);
    } catch (err) {
      console.error('Failed to load emails:', err);
    } finally {
      setEmailsLoading(false);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }, []);

  const handleFetchEmails = async () => {
    setFetchLoading(true);
    setError(null);
    try {
      await fetchEmailsFromGmail();
      await loadEmails();
      await loadStats();
    } catch (err) {
      console.error('Failed to fetch emails:', err);
      setError(err.message || 'Failed to fetch emails. Check the backend terminal for details.');
      setTimeout(() => setError(null), 10000);
    } finally {
      setFetchLoading(false);
    }
  };

  // Load data on mount
  useEffect(() => {
    loadEmails();
    loadStats();
  }, [loadEmails, loadStats]);

  const handleNavigate = (view) => {
    setActiveView(view);
    setSelectedEmailId(null);
  };

  const handleEmailSelect = (id) => {
    setSelectedEmailId(id);
  };

  const handleSuggestionUpdate = () => {
    loadStats();
  };

  const currentView = VIEW_TITLES[activeView];

  return (
    <div className="app-layout">
      <Sidebar
        activeView={activeView}
        onNavigate={handleNavigate}
        stats={stats}
      />

      <div className="main-area">
        <Header
          title={currentView.title}
          subtitle={currentView.subtitle}
          onRefresh={handleFetchEmails}
          loading={fetchLoading}
        />

        {error && (
          <div style={{
            background: 'rgba(244, 63, 94, 0.15)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            color: '#fda4af',
            padding: '12px 20px',
            fontSize: '13px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
          }}>
            <span>⚠️</span>
            <span style={{ flex: 1 }}>{error}</span>
            <button
              onClick={() => setError(null)}
              style={{
                background: 'none',
                border: 'none',
                color: '#fda4af',
                cursor: 'pointer',
                fontSize: '16px',
              }}
            >✕</button>
          </div>
        )}

        {activeView === 'inbox' && (
          <div className="inbox-layout">
            <EmailList
              emails={emails}
              selectedId={selectedEmailId}
              onSelect={handleEmailSelect}
              loading={emailsLoading}
            />
            <EmailDetail
              emailId={selectedEmailId}
              onUpdate={handleSuggestionUpdate}
            />
          </div>
        )}

        {activeView === 'tasks' && (
          <div className="page-content">
            <TaskBoard />
          </div>
        )}

        {activeView === 'followups' && (
          <div className="page-content">
            <FollowUpTracker />
          </div>
        )}
      </div>
    </div>
  );
}
