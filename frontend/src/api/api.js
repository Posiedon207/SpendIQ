import axios from 'axios'

// API base URL — uses relative path so nginx can proxy correctly
// In development, Vite proxies /api to localhost:8000
// In production (Docker/K8s), nginx proxies /api to the backend service
const API_BASE = ''

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// Response interceptor for error normalization
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

// ─── Transaction API ─────────────────────────────────────────────────────────

export const transactionsApi = {
  list: (params = {}) => api.get('/api/transactions', { params }),
  get: (id) => api.get(`/api/transactions/${id}`),
  create: (data) => api.post('/api/transactions', data),
  update: (id, data) => api.put(`/api/transactions/${id}`, data),
  delete: (id) => api.delete(`/api/transactions/${id}`),
}

// ─── Budget API ──────────────────────────────────────────────────────────────

export const budgetsApi = {
  list: (params = {}) => api.get('/api/budgets', { params }),
  get: (id) => api.get(`/api/budgets/${id}`),
  create: (data) => api.post('/api/budgets', data),
  update: (id, data) => api.put(`/api/budgets/${id}`, data),
  delete: (id) => api.delete(`/api/budgets/${id}`),
}

// ─── Analytics API ───────────────────────────────────────────────────────────

export const analyticsApi = {
  get: (params = {}) => api.get('/api/analytics', { params }),
}

// ─── Health API ──────────────────────────────────────────────────────────────

export const healthApi = {
  check: () => api.get('/health'),
  ready: () => api.get('/ready'),
}

// ─── Utility API ─────────────────────────────────────────────────────────────

export const utilityApi = {
  seed: () => api.post('/api/seed'),
}

export default api
