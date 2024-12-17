import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/servis_api/usuarios/',  // Ajustar esto a la URL de tu API en Django
  headers: {
    'Content-Type': 'application/json',
  },
});
// Configuración de JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});


export default api;
