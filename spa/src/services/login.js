import axios from './base';

export default {
  login (login, password) {
    let data = {login, password};
    return axios
      .post('/login', data)
      .then((response) => {
        let token = response.data.token;
        axios.defaults.headers['Authorization'] = `Socek ${token}`;
      });
  }
}
