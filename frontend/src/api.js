// configures the necessary authorisation header and content type to allow for use of the api from the frontend
// resuable API utility to handle requests to the FastAPI backend 
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Your FastAPI URL

// Function to get the access token from localStorage
export const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Axios instance with authorization header
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add the Authorization header if the token is available
api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
