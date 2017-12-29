import Transaction from '@/models/transaction';
import axios from './base';

export default {
  get (params) {
    return axios
      .get('/transactions', {params: params})
      .then((response) => {
        let transactions = response.data.transactions;
        let sumLeft = 0;
        transactions.forEach(Transaction.computeLeftCost);
        transactions.forEach((obj) => { sumLeft += obj.left; });
        response.data.sumLeft = sumLeft;
        return response;
      });
  },
  upload (file) {
    let data = new FormData();
    data.append('file', file);
    return axios.post('/transactions/upload', data)
  }
}
