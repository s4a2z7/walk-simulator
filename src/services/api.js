import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

// Helper to get token from localStorage
const getToken = () => localStorage.getItem('token');

// Create axios instance with default headers
const axiosInstance = axios.create({
  baseURL: API_URL
});

// Add token to requests
axiosInstance.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data) => axiosInstance.post('/auth/register', data),
  login: (data) => axiosInstance.post('/auth/login', data),
  getCurrentUser: () => axiosInstance.get('/auth/me'),
};

// Pet API
export const petAPI = {
  getPet: () => axiosInstance.get('/pet'),
  getPetStatus: () => axiosInstance.get('/pet/status'),
  addSteps: (steps) => axiosInstance.post('/pet/steps', { steps }),
  feedPet: (food_type) => axiosInstance.post('/pet/feed', { food_type }),
  updatePetName: (name) => axiosInstance.patch('/pet/name', { name }),
};

// Ranking API
export const rankingAPI = {
  getRanking: (limit = 10) => axiosInstance.get(`/ranking?limit=${limit}`),
  getLeaderboard: (limit = 50) => axiosInstance.get(`/ranking/leaderboard?limit=${limit}`),
  addFriend: (username) => axiosInstance.post('/ranking/friends', { username }),
  getFriends: () => axiosInstance.get('/ranking/friends'),
  removeFriend: (friendshipId) => axiosInstance.delete(`/ranking/friends/${friendshipId}`),
};

// Statistics API
export const statisticsAPI = {
  getTodayStats: () => axiosInstance.get('/statistics/today'),
  getHistory: (days = 7) => axiosInstance.get(`/statistics/history?days=${days}`),
  getEvolutions: () => axiosInstance.get('/statistics/evolutions'),
  getFeedings: (limit = 20) => axiosInstance.get(`/statistics/feedings?limit=${limit}`),
};
// Allergy API
export const allergyAPI = {
  setAllergies: (allergies) => axiosInstance.post('/allergy/allergies', { allergies }),
  getAllergies: () => axiosInstance.get('/allergy/allergies'),
  checkAllergy: (imageBase64, ocrText) => 
    axiosInstance.post('/allergy/check', { imageBase64, ocrText }),
  getCheckHistory: (limit = 10) => 
    axiosInstance.get(`/allergy/history?limit=${limit}`),
};