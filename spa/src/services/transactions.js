import axios from './base';

export default {
  get () {
    return axios.get('/transactions');
  }
}
