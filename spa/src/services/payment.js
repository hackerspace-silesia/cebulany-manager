import axios from './base';
import {downloadFile} from './excel';

export default {
  getAll (params) {
    return axios.get('/payment/', {params});
  },
  getTable (params) {
    return axios.get('/payment/table', {params});
  },
  getExcelTable (yearStart, yearEnd, paymentTypeId) {
    return axios.get(
      `/excel/table/${yearStart}-${yearEnd}/${paymentTypeId}`,
      { responseType: 'blob' }
    ).then(downloadFile);
  },
  getExcel (params) {
    return axios.get(
      `/excel/payment/`,
      { responseType: 'blob', params }
    ).then(downloadFile);
  },
  getSummary (params) {
    return axios.get('/payment/summary', {params});
  },
  getExcelSummary (year) {
    return axios.get(
      `/excel/summary/${year}`,
      { responseType: 'blob' }
    ).then(downloadFile);
  },
  post (data) {
    return axios.post('/payment/', data);
  },
  delete (id) {
    return axios.delete(`/payment/${id}`);
  }
}
