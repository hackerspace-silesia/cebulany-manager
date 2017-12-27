import axios from './base';

export default {
  get ({query, limit = 5}) {
    let params = {q: query, limit: limit};
    return axios.get('/members', {params});
  },
  getAll () {
    return axios.get('/members');
  },
  create (data) {
    return axios.post(`/members`, data);
  },
  update (id, data) {
    return axios.put(`/members/${id}`, data);
  }
}
