import Transaction from '@/models/transaction';
import axios from './base';

export default {
  get () {
    return axios
      .get('/transactions')
      .then((response) => {
        let transactions = response.data.transactions;
        let sumLeft = 0;
        transactions.forEach(Transaction.computeLeftCost);
        transactions.forEach((obj) => { sumLeft += obj.left; });
        response.data.sumLeft = sumLeft;
        return response;
      });
  }
}
