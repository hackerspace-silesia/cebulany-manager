import axios from './base';

export default {
  getToken (login, password, token) {
    let data = {login, password, token};
    return axios
      .post('/login', data)
      .then(response => response.data);
  },
  loginFromSession () {
    const token = localStorage.token;
    if (!token) {
      return false;
    }
    this.setHeader(token);
    return true;
  },
  setTokenIntoSession (token, tokenTime) {
    localStorage.token = token;
    localStorage.tokenTime = tokenTime;
    this.setHeader(token);
  },
  logout () {
    localStorage.removeItem('token');
    localStorage.removeItem('tokenTime');
  },
  setHeader (token) {
    axios.defaults.headers['Authorization'] = `Socek ${token}`;
  }
};
