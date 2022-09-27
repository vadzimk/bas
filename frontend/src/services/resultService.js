import api from "./api";

export const getAllResults = async () => {
    const res = await api.get('/jobs')
    return res.data
}

export const getResults = async (model_ids, user_id) => {
    const res = await api.get('/jobs', {
        params: {
            model_id: model_ids,
            user_id
        },
    })
    return res.data
}

export const updateResultsRow = async (recordToSend, model_ids, user_id) => {
    const res = await api.put('/job', {record: recordToSend, user_id, model_ids})
    return res.data
}

