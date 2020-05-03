import axios from './base';

export default {
  getAll (params) {
    return axios.get('/payment/', {params: params});
  },
  getTable (params) {
    return axios.get('/payment/table', {params: params});
  },
  getSummary (params) {
    return axios.get('/payment/summary', {params: params});
  },
  post (data) {
    return axios.post('/payment/', data);
  },
  delete (id) {
    return axios.delete(`/payment/${id}`);
  }
}
