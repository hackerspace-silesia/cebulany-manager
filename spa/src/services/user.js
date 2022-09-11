import axios from './base';

export default {
  getAll (params) {
    params = params || {};
    return axios.get('/user/', {params: params});
  },
  create (data) {
    return axios.post('/user/', data);
  },
  update (id, data) {
    return axios.put(`/user/${id}`, data);
  },
  delete (id) {
    return axios.delete(`/user/${id}`);
  },
  changePassword (id, password) {
    const data = { password };
    return axios.post(`/user/${id}/password`, data);
  },
}
