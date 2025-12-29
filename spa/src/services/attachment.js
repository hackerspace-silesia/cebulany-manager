import axios from './base';

export default {
  post (data) {
    return axios.post('/attachment/', data);
  },
  put (id, data) {
    return axios.put(`/attachment/${id}`, data);
  },
  delete (id) {
    return axios.delete(`/attachment/${id}`);
  },
}
