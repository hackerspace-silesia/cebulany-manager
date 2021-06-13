import axios from './base';

export default {
  getAll (params) {
    return axios.get('/payment/', {params: params});
  },
  getTable (params) {
    return axios.get('/payment/table', {params: params});
  },
  getExcelTable (yearStart, yearEnd, paymentTypeId) {
    return axios.get(
      `/excel/table/${yearStart}-${yearEnd}/${paymentTypeId}`,
      { responseType: 'blob' }
    ).then((response) => {
      // the most retard way.
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'wtf.xlsx');
      document.body.appendChild(link);
      link.click();
    });
  },
  getSummary (params) {
    return axios.get('/payment/summary', {params: params});
  },
  post (data) {
    return axios.post('/payment/', data);
  },
  delete (id) {
    return axios.delete(`/payment/${id}`);
  }
}
