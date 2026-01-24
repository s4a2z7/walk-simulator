import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL;

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
  getPet: async () => {
    if (!API_BASE_URL) {
      // MOCK: API 주소가 없으면 데모용 데이터 반환
      return {
        data: {
          pet: {
            name: '데모펫',
            stage_emoji: '🐶',
            stage_name: '아기',
            total_exp: 100,
            total_steps: 5000,
            age_days: 3,
            current_stage: 1,
            exp_to_next_stage: 200,
            current_exp: 100,
            user_id: 'demo',
          },
        },
      };
    }
    return api.get('/pet');
  },
  addSteps: (steps) => API_BASE_URL ? api.post('/pet/steps', { steps }) : Promise.resolve({ data: { pet: { ...petAPI._mockPet, total_steps: (petAPI._mockPet?.total_steps || 0) + steps } } }),
  feedPet: (food_type) => API_BASE_URL ? api.post('/pet/feed', { food_type }) : Promise.resolve({ data: {} }),
  updateName: (name) => API_BASE_URL ? api.patch('/pet/name', { name }) : Promise.resolve({ data: {} }),
  getStatus: () => API_BASE_URL ? api.get('/pet/status') : Promise.resolve({ data: {} }),
  drinkWater: (amount_ml = 200) => API_BASE_URL ? api.post('/pet/drink-water', { amount_ml }) : Promise.resolve({ data: {} }),
  stretch: (exp_gained = 5) => API_BASE_URL ? api.post('/pet/stretch', { exp_gained }) : Promise.resolve({ data: {} }),
  sleepEarly: (exp_gained = 10) => API_BASE_URL ? api.post('/pet/sleep-early', { exp_gained }) : Promise.resolve({ data: {} }),
  _mockPet: {
    name: '데모펫',
    stage_emoji: '🐶',
    stage_name: '아기',
    total_exp: 100,
    total_steps: 5000,
    age_days: 3,
    current_stage: 1,
    exp_to_next_stage: 200,
    current_exp: 100,
    user_id: 'demo',
  },
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
