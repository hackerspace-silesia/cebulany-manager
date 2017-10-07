import axios from './base';

export default {
  post ({transaction_id, member_id, date, cost}) {
    return axios.post('/paid_month', {transaction_id, member_id, date, cost})
  },
  delete (id) {
    return axios.delete(`/paid_month/${id}`)
  }
}
