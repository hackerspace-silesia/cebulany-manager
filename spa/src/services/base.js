import stateData from '@/state';
import axios from 'axios';

const base = axios.create({
  baseURL: process.env.API_URL,
  timeout: 5000,
  maxRedirects: 0
})

base.interceptors.response.use((response) => {
  stateData.updateDeadline();
  return response;
});

export default base;
