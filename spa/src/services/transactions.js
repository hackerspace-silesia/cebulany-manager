import Transaction from '@/models/transaction';
import axios from './base';
import {downloadFile} from './excel';

export default {
  getAll (params) {
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
  get (id) {
    return axios.get(`/transactions/${id}`)
      .then((response) => {
        Transaction.computeLeftCost(response.data);
        return response;
      });
  },
  put (id, data) {
    return axios.put(`/transactions/${id}`, data)
      .then((response) => {
        Transaction.computeLeftCost(response.data);
        return response;
      });
  },
  getExcelTable (month) {
    return axios.get(
      `/excel/transactions/${month}`,
      { responseType: 'blob' }
    ).then(downloadFile);
  },
  upload (file) {
    let data = new FormData();
    data.append('file', file);
    return axios.post('/transactions/upload', data)
  }
}
