import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API || 'http://127.0.0.1:5000',
});

export default api;