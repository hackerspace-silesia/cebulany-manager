import axios from './base';

function downloadFile(response) {
  // the most retard way.
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  const contentDisposition = response.headers['content-disposition'] || '';
  console.log(contentDisposition);
  const match = contentDisposition.match(/filename="?([\w_.-]+)"?/);
  const filename = match ? match[1] : 'file.xlsx';
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
}

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
    ).then(downloadFile);
  },
  getSummary (params) {
    return axios.get('/payment/summary', {params: params});
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
