import axios from './base';

export class SimpleService {
  constructor(path) {
    this.path = path;
  }

  getAll (params) {
    params = params || {};
    return axios.get(this.path, {params: params});
  }

  post (data) {
    return axios.post(this.path, data);
  }

  update (id, data) {
    return axios.put(`${this.path}/${id}`, data);
  }

  delete (id) {
    return axios.delete(`${this.path}/${id}`);
  }
}