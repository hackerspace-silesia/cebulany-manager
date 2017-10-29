import axios from './base';

export default {
  getAll (params) {
    params = params || {};
    return axios.get('/donation', {params: params});
  },
  post ({transaction_id, cost, name}) {
    return axios.post('/donation', {transaction_id, cost, name});
  },
  delete (id) {
    return axios.delete(`/donation/${id}`);
  }
}
