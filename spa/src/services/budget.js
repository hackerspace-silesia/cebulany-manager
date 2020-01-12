import axios from './base';

export default {
  getAll (params) {
    params = params || {};
    return axios.get('/budget/', {params: params});
  },
  post (data) {
    return axios.post('/budget/', data);
  },
  update (id, data) {
    return axios.put(`/budget/${id}`, data);
  },
  delete (id) {
    return axios.delete(`/budget/${id}`);
  }
}
