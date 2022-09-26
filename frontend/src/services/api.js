import axios from 'axios'
import qs from 'qs'

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    },
    paramsSerializer: params => {
        return qs.stringify(params, {arrayFormat: "repeat"})
    }
})


export default api