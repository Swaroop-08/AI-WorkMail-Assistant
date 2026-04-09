import StatusBadge from './StatusBadge';

export default function TaskCard({ task, onStatusChange }) {
  const handleStatusChange = (e) => {
    onStatusChange(task.id, e.target.value);
  };

  return (
    <div className="task-card animate-fade-in-up">
      <div className="task-card-header">
        <span className="task-card-type">{task.task_type}</span>
        <StatusBadge type="priority" value={task.priority} />
      </div>

      <p className="task-card-description">{task.description}</p>

      <div className="task-card-meta">
        {task.deadline && (
          <span className="task-meta-item">
            <span className="task-meta-icon">📅</span>
            {task.deadline}
          </span>
        )}
        {task.people_involved && (
          <span className="task-meta-item">
            <span className="task-meta-icon">👤</span>
            {task.people_involved}
          </span>
        )}
      </div>

      <div className="task-card-footer">
        <span className="task-card-source" title={task.email_subject}>
          ✉️ {task.email_sender || 'Unknown'} 
        </span>
        <select
          className="task-status-select"
          value={task.status}
          onChange={handleStatusChange}
          id={`task-status-${task.id}`}
        >
          <option value="todo">📋 To Do</option>
          <option value="in_progress">🔧 In Progress</option>
          <option value="done">✅ Done</option>
        </select>
      </div>
    </div>
  );
}
