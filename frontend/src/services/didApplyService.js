import api from "./api";

export const getDidApply = async (model_ids, user_id) => {
    const res = await api.get('/jobs/did-apply', {
        params: {
            user_id
        },
    })
    return res.data
}

export const updateDidAppyRow = async (recordToSend, model_ids, user_id) => {
    const res = await api.put('/jobs/did-apply', {record: recordToSend, user_id})
    return res.data
}