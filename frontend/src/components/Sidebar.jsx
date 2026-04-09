export default function Sidebar({ activeView, onNavigate, stats }) {
  const navItems = [
    {
      id: 'inbox',
      label: 'Inbox',
      icon: '📨',
      badge: stats?.total_emails || 0,
      badgeType: '',
    },
    {
      id: 'tasks',
      label: 'Tasks',
      icon: '✅',
      badge: stats?.pending_tasks || 0,
      badgeType: '',
    },
    {
      id: 'followups',
      label: 'Follow-Ups',
      icon: '🔔',
      badge: stats?.pending_followups || 0,
      badgeType: stats?.pending_followups > 0 ? 'warning' : '',
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">AI</div>
          <div>
            <div className="sidebar-logo-text">Inbox Executive</div>
            <div className="sidebar-logo-sub">AI-Powered Assistant</div>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <div
            key={item.id}
            className={`sidebar-nav-item ${activeView === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
            role="button"
            tabIndex={0}
            id={`nav-${item.id}`}
          >
            <span className="sidebar-nav-icon">{item.icon}</span>
            <span>{item.label}</span>
            {item.badge > 0 && (
              <span className={`sidebar-badge ${item.badgeType}`}>
                {item.badge}
              </span>
            )}
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-mode-badge">
          <span className="sidebar-mode-dot"></span>
          <span>Demo Mode Active</span>
        </div>
      </div>
    </aside>
  );
}
