import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 15000
});

export async function predictUrl(url, includeContent = true) {
  const response = await api.post('/api/predict', {
    url,
    include_content: includeContent
  });
  return response.data;
}

export default api;
