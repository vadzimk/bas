import api from './api'

export const createSearch = async (newSearch) => {
    const res = await api.post('/search', newSearch)
    return res.status
}