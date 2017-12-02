import axios from 'axios';

export default axios.create({
  baseURL: process.env.API_URL,
  timeout: 5000,
  maxRedirects: 0
})
