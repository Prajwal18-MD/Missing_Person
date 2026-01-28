import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getProfile: () => api.get('/auth/me'),
};

export const casesAPI = {
  create: (formData) => api.post('/cases/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAll: () => api.get('/cases/'),
  getById: (id) => api.get(`/cases/${id}`),
  update: (id, data) => api.put(`/cases/${id}`, data),
  delete: (id) => api.delete(`/cases/${id}`),
};

export const sightingsAPI = {
  upload: (formData) => api.post('/sightings/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAll: () => api.get('/sightings/'),
  getById: (id) => api.get(`/sightings/${id}`),
  reprocess: (id) => api.post(`/sightings/${id}/reprocess`),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getAllCases: () => api.get('/admin/cases'),
  getCaseDetails: (id) => api.get(`/admin/cases/${id}`),
  markFound: (id) => api.put(`/admin/cases/${id}/found`),
  getAllMatches: (verified = null) => {
    const params = verified !== null ? { verified } : {};
    return api.get('/admin/matches', { params });
  },
  updateMatch: (id, data) => api.put(`/admin/matches/${id}`, data),
  getLocationHistory: (caseId) => api.get(`/admin/cases/${caseId}/location-history`),
  deleteCase: (id) => api.delete(`/admin/cases/${id}`),
};

export default api;