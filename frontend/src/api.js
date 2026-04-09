const API_BASE = import.meta.env.DEV ? 'http://localhost:8000/api' : '/_/backend/api';

async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

// ─── Email Endpoints ───
export const fetchEmailsFromGmail = () => apiFetch('/emails/fetch', { method: 'POST' });
export const getEmails = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return apiFetch(`/emails${query ? '?' + query : ''}`);
};
export const getEmailDetail = (id) => apiFetch(`/emails/${id}`);
export const getEmailSuggestions = (id) => apiFetch(`/emails/${id}/suggestions`);
export const approveSuggestion = (emailId, suggestionId) =>
  apiFetch(`/emails/${emailId}/suggestions/${suggestionId}/approve`, { method: 'POST' });
export const dismissSuggestion = (emailId, suggestionId) =>
  apiFetch(`/emails/${emailId}/suggestions/${suggestionId}/dismiss`, { method: 'POST' });

// ─── Task Endpoints ───
export const getTasks = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return apiFetch(`/tasks${query ? '?' + query : ''}`);
};
export const getTaskStats = () => apiFetch('/tasks/stats');
export const updateTaskStatus = (id, status) =>
  apiFetch(`/tasks/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });

// ─── Follow-Up Endpoints ───
export const getFollowUps = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return apiFetch(`/followups${query ? '?' + query : ''}`);
};
export const scanFollowUps = () => apiFetch('/followups/scan', { method: 'POST' });
export const approveFollowUp = (id) => apiFetch(`/followups/${id}/approve`, { method: 'POST' });
export const dismissFollowUp = (id) => apiFetch(`/followups/${id}/dismiss`, { method: 'POST' });

// ─── Stats ───
export const getStats = () => apiFetch('/stats');

// ─── Reset ───
export const resetData = () => apiFetch('/reset', { method: 'DELETE' });
