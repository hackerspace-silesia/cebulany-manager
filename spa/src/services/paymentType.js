import axios from './base';

export default {
  getAll (params) {
    params = params || {};
    return axios.get('/payment_type/', {params: params});
  },
  post (data) {
    return axios.post('/payment_type/', data);
  },
  update (id, data) {
    return axios.put(`/payment_type/${id}`, data);
  },
  delete (id) {
    return axios.delete(`/payment_type/${id}`);
  }
}
