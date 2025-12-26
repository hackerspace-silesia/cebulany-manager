import axios from './base';

export default {
    getAll(params) {
        return axios.get('/document/', { params });
    },
    sync(month) {
        return axios.post(`/document/sync/${month}`);
    },
    update(id, data) {
        return axios.put(`/document/${id}`, data);
    },
}
