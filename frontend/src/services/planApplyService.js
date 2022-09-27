import api from "./api";

export const getPlanApply = async (model_ids, user_id) => {
    const res = await api.get('/jobs/plan-apply', {
        params: {
            user_id
        },
    })
    return res.data
}

export const updatePlanAppyRow = async (recordToSend, model_ids, user_id) => {
    const res = await api.put('/jobs/plan-apply', {record: recordToSend, user_id})
    return res.data
}