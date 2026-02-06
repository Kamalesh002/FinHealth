import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
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
let isRedirecting = false;
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && !isRedirecting) {
            // Don't redirect if we're already on login/register pages
            const currentPath = window.location.pathname;
            if (!currentPath.includes('/login') && !currentPath.includes('/register')) {
                isRedirecting = true;
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data) => api.post('/auth/register', data),
    login: (data) => {
        const formData = new URLSearchParams();
        formData.append('username', data.email);
        formData.append('password', data.password);
        return api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
    },
    getProfile: () => api.get('/auth/me'),
    updateProfile: (data) => api.put('/auth/me', null, { params: data })
};

// Company API
export const companyAPI = {
    create: (data) => api.post('/upload/company', data),
    getAll: () => api.get('/upload/companies'),
    getById: (id) => api.get(`/upload/company/${id}`)
};

// Upload API
export const uploadAPI = {
    uploadFile: (companyId, file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post(`/upload/file/${companyId}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    validate: (data) => api.post('/upload/validate', data),
    getPending: (companyId) => api.get(`/upload/pending/${companyId}`)
};

// Analysis API
export const analysisAPI = {
    getHealthScore: (companyId, recalculate = false) =>
        api.get(`/analysis/health-score/${companyId}`, { params: { recalculate } }),
    getSummary: (companyId) => api.get(`/analysis/summary/${companyId}`),
    getBenchmark: (companyId) => api.get(`/analysis/benchmark/${companyId}`),
    getForecast: (companyId) => api.get(`/analysis/forecast/${companyId}`),
    getProductRecommendations: (companyId) => api.get(`/analysis/products/${companyId}`),
    getAllProducts: () => api.get('/analysis/products'),
    downloadReport: (companyId) => api.get(`/analysis/report/${companyId}`, { responseType: 'blob' }),
    // NEW: Competition-Winning Features
    getRiskAlerts: (companyId) => api.get(`/analysis/risk-alerts/${companyId}`),
    getCFOInsights: (companyId) => api.get(`/analysis/cfo-insights/${companyId}`),
    getActionPlan: (companyId) => api.get(`/analysis/action-plan/${companyId}`)
};

// Chat API
export const chatAPI = {
    query: (data) => api.post('/chat/query', data),
    getSuggestions: (companyId) => api.get(`/chat/suggested-questions/${companyId}`)
};

export default api;
