import axios from './base';

export default {
  getToken (login, password, token) {
    let data = {login, password, token};
    return axios
      .post('/login', data)
      .then(response => response.data);
  },
  loginFromSession () {
    const token = sessionStorage.token;
    if (!token) {
      return false;
    }
    this.setHeader(token);
    return true;
  },
  setTokenIntoSession (token, tokenTime) {
    sessionStorage.token = token;
    sessionStorage.tokenTime = tokenTime;
    this.setHeader(token);
  },
  logout () {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('tokenTime');
  },
  setHeader (token) {
    axios.defaults.headers['Authorization'] = `Socek ${token}`;
  }
};
