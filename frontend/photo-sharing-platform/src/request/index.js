import axios from 'axios'

function getRequest(url, params) {
    return new Promise((resolve, reject) => {
        axios
            .get(url, {
                params
            })
            .then(response => {
                resolve(response.data);
            })
            .catch(err => {
                reject(err);
            })
    })
}

function postRequest(url, params) {
    return new Promise((resolve, reject) => {
        axios
            .post(url, params)
            .then(response => {
                console.log(response.data)
                resolve(response.data);
            })
            .catch(err => {
                reject(err);
            })
    })
}

function putRequest(url, params) {
    return new Promise((resolve, reject) => {
        axios
            .put(url, params)
            .then(response => {
                resolve(response.data);
            })
            .catch(err => {
                reject(err);
            })
    })
}

function deleteRequest(url, params) {
    return new Promise((resolve, reject) => {
        axios
            .delete(url, {
                params
            })
            .then(response => {
                resolve(response.data);
            })
            .catch(err => {
                reject(err);
            })
    })
}

// eslint-disable-next-line import/no-anonymous-default-export
export default {
    getRequest,
    postRequest,
    putRequest,
    deleteRequest
}