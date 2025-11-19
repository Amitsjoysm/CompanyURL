import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${API_URL}/api`;

// Create axios instance
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle auth errors
apiClient.interceptors.response.use(
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

export const auth = {
  register: (data) => apiClient.post('/auth/register', data),
  login: (data) => apiClient.post('/auth/login', data),
  getMe: () => apiClient.get('/auth/me'),
};

export const crawl = {
  single: (data) => apiClient.post('/crawl/single', data),
  getRequest: (id) => apiClient.get(`/crawl/request/${id}`),
  getHistory: (limit = 50) => apiClient.get(`/crawl/history?limit=${limit}`),
  search: (query, limit = 10) => apiClient.get(`/crawl/search?query=${query}&limit=${limit}`),
  bulkCheck: (formData) => apiClient.post('/crawl/bulk-check', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  bulkUpload: (formData) => apiClient.post('/crawl/bulk-upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
};

export const payment = {
  getPlans: () => apiClient.get('/payment/plans'),
  createOrder: (data) => apiClient.post('/payment/create-order', data),
  verify: (data) => apiClient.post('/payment/verify', data),
  getRazorpayKey: () => apiClient.get('/payment/razorpay-key'),
};

export const content = {
  getBlogs: () => apiClient.get('/content/blogs'),
  getBlog: (slug) => apiClient.get(`/content/blogs/${slug}`),
  getFaqs: () => apiClient.get('/content/faqs'),
  
  // Admin endpoints
  createBlog: (data) => apiClient.post('/content/blogs', data),
  updateBlog: (slug, data) => apiClient.put(`/content/blogs/${slug}`, data),
  deleteBlog: (slug) => apiClient.delete(`/content/blogs/${slug}`),
  createFaq: (data) => apiClient.post('/content/faqs', data),
  updateFaq: (id, data) => apiClient.put(`/content/faqs/${id}`, data),
  deleteFaq: (id) => apiClient.delete(`/content/faqs/${id}`),
};

export const admin = {
  // Users management
  getUsers: () => apiClient.get('/admin/users'),
  updateUserCredits: (userId, data) => apiClient.put(`/admin/users/${userId}/credits`, data),
  updateUserStatus: (userId, data) => apiClient.put(`/admin/users/${userId}/status`, data),
  
  // Plans management
  createPlan: (data) => apiClient.post('/admin/plans', data),
  updatePlan: (planId, data) => apiClient.put(`/admin/plans/${planId}`, data),
  deletePlan: (planId) => apiClient.delete(`/admin/plans/${planId}`),
  
  // Central ledger
  getCentralLedger: (limit = 100) => apiClient.get(`/admin/central-ledger?limit=${limit}`),
};

export const apiTokens = {
  list: () => apiClient.get('/api-tokens'),
  create: (data) => apiClient.post('/api-tokens', data),
  revoke: (tokenId) => apiClient.delete(`/api-tokens/${tokenId}`),
  toggle: (tokenId) => apiClient.put(`/api-tokens/${tokenId}/toggle`),
};

export default apiClient;
