import axios from './base';

export default {
  post ({transaction_id, cost, name}) {
    return axios.post('/bill', {transaction_id, cost, name})
  },
  delete (id) {
    return axios.delete(`/bill/${id}`)
  }
}
