import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
};

// Pet API
export const petAPI = {
  getPet: () => api.get('/pet'),
  addSteps: (steps) => api.post('/pet/steps', { steps }),
  feedPet: (food_type) => api.post('/pet/feed', { food_type }),
  updateName: (name) => api.patch('/pet/name', { name }),
  getStatus: () => api.get('/pet/status'),
  drinkWater: (amount_ml = 200) => api.post('/pet/drink-water', { amount_ml }),
  stretch: (exp_gained = 5) => api.post('/pet/stretch', { exp_gained }),
  sleepEarly: (exp_gained = 10) => api.post('/pet/sleep-early', { exp_gained }),
};

// Ranking API
export const rankingAPI = {
  getRanking: (limit = 10) => api.get(`/ranking?limit=${limit}`),
  getLeaderboard: (limit = 50) => api.get(`/ranking/leaderboard?limit=${limit}`),
  getFriends: () => api.get('/ranking/friends'),
  addFriend: (username) => api.post('/ranking/friends', { username }),
  removeFriend: (friendshipId) => api.delete(`/ranking/friends/${friendshipId}`),
};

// Statistics API
export const statisticsAPI = {
  getTodayStats: () => api.get('/statistics/today'),
  getHistory: (days = 7) => api.get(`/statistics/history?days=${days}`),
  getEvolutions: () => api.get('/statistics/evolutions'),
  getFeedings: (limit = 20) => api.get(`/statistics/feedings?limit=${limit}`),
};

export default api;
