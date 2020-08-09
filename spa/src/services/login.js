import axios from './base';

export default {
  getToken (login, password, token) {
    let data = {login, password, token};
    return axios
      .post('/login', data)
      .then(response => response.data.token);
  },
  loginFromSession () {
    const token = sessionStorage.token;
    if (!token) {
      return false;
    }
    this.setHeader(token);
    return true;
  },
  setTokenIntoSession (token) {
    sessionStorage.token = token;
    this.setHeader(token);
  },
  setHeader (token) {
    axios.defaults.headers['Authorization'] = `Socek ${token}`;
  }
};
