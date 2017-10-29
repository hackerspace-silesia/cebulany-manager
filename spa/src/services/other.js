import axios from './base';

export default {
  getAll (params) {
    params = params || {};
    return axios.get('/other', {params: params});
  },
  post ({transaction_id, cost, name}) {
    return axios.post('/other', {transaction_id, cost, name});
  },
  delete (id) {
    return axios.delete(`/other/${id}`);
  }
}
