import axios from 'axios';

export default {
  get () {
    return axios.get('http://127.0.0.1:5000/api/transactions');
  }
}
