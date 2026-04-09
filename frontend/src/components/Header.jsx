export default function Header({ title, subtitle, onRefresh, loading }) {
  return (
    <header className="header">
      <div className="header-left">
        <div>
          <h1 className="header-title">{title}</h1>
          {subtitle && <p className="header-subtitle">{subtitle}</p>}
        </div>
      </div>
      <div className="header-right">
        <button
          className={`btn btn-primary ${loading ? 'btn-loading' : ''}`}
          onClick={onRefresh}
          disabled={loading}
          id="btn-refresh"
        >
          <span className={loading ? 'btn-spinner' : ''}>
            {loading ? '⟳' : '🔄'}
          </span>
          {loading ? 'Fetching...' : 'Fetch Emails'}
        </button>
      </div>
    </header>
  );
}
