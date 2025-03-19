import { SimpleService } from './simple';

class UserService extends SimpleService {
  constructor() {
    super('/user');
  }

  changePassword(id, password) {
    const data = { password };
    return axios.post(`${this.path}/${id}/password`, data);
  }
};

export default new UserService();