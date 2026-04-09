import { useState, useEffect } from 'react';
import { getTasks, updateTaskStatus, getTaskStats } from '../api';
import TaskCard from './TaskCard';
import LoadingSpinner from './LoadingSpinner';

export default function TaskBoard() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [priorityFilter, setPriorityFilter] = useState('all');

  const loadTasks = async () => {
    setLoading(true);
    try {
      const [tasksData, statsData] = await Promise.all([
        getTasks(),
        getTaskStats(),
      ]);
      setTasks(tasksData);
      setStats(statsData);
    } catch (err) {
      console.error('Failed to load tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await updateTaskStatus(taskId, newStatus);
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
      );
      // Refresh stats
      const newStats = await getTaskStats();
      setStats(newStats);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const filteredTasks = tasks.filter((task) => {
    if (priorityFilter === 'all') return true;
    return task.priority === priorityFilter;
  });

  const columns = [
    { id: 'todo', title: 'To Do', icon: '📋' },
    { id: 'in_progress', title: 'In Progress', icon: '🔧' },
    { id: 'done', title: 'Done', icon: '✅' },
  ];

  if (loading) {
    return <LoadingSpinner text="Loading tasks..." />;
  }

  return (
    <div className="task-board">
      {/* Stats */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card violet">
            <div className="stat-icon violet">📋</div>
            <div className="stat-info">
              <div className="stat-value">{stats.total}</div>
              <div className="stat-label">Total Tasks</div>
            </div>
          </div>
          <div className="stat-card amber">
            <div className="stat-icon amber">⏳</div>
            <div className="stat-info">
              <div className="stat-value">{stats.todo + stats.in_progress}</div>
              <div className="stat-label">Pending</div>
            </div>
          </div>
          <div className="stat-card emerald">
            <div className="stat-icon emerald">✅</div>
            <div className="stat-info">
              <div className="stat-value">{stats.done}</div>
              <div className="stat-label">Completed</div>
            </div>
          </div>
          <div className="stat-card rose">
            <div className="stat-icon rose">🔴</div>
            <div className="stat-info">
              <div className="stat-value">{stats.high_priority}</div>
              <div className="stat-label">High Priority</div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="task-filters">
        {['all', 'high', 'medium', 'low'].map((p) => (
          <button
            key={p}
            className={`filter-chip ${priorityFilter === p ? 'active' : ''}`}
            onClick={() => setPriorityFilter(p)}
          >
            {p === 'all' ? 'All Priorities' :
             p === 'high' ? '🔴 High' :
             p === 'medium' ? '🟡 Medium' : '🟢 Low'}
          </button>
        ))}
      </div>

      {/* Kanban Columns */}
      {filteredTasks.length === 0 ? (
        <div className="empty-state">
          <span className="empty-state-icon">📋</span>
          <span className="empty-state-title">No tasks yet</span>
          <span className="empty-state-text">
            Fetch emails and AI will automatically extract tasks
          </span>
        </div>
      ) : (
        <div className="task-columns">
          {columns.map((col) => {
            const columnTasks = filteredTasks.filter((t) => t.status === col.id);
            return (
              <div key={col.id} className="task-column">
                <div className="task-column-header">
                  <div className="task-column-title">
                    <span className={`task-column-dot ${col.id}`}></span>
                    {col.icon} {col.title}
                  </div>
                  <span className="task-column-count">{columnTasks.length}</span>
                </div>
                <div className="task-column-items stagger-children">
                  {columnTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onStatusChange={handleStatusChange}
                    />
                  ))}
                  {columnTasks.length === 0 && (
                    <div className="empty-state" style={{ padding: '2rem 1rem' }}>
                      <span style={{ fontSize: '1.5rem', opacity: 0.3 }}>{col.icon}</span>
                      <span className="empty-state-text">No tasks</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
