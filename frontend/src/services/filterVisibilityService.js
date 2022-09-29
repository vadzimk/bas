import api from "./api";

export const getFilteredCompanies = async (user_id) => {
    const res = await api.get('/filter-visibility/company', {
        params: {
            user_id
        },
    })
    return res.data
}

export const unfilterCompany = async (company_id, user_id) => {
    const res = await api.put('/filter-visibility/company', {company_id, user_id})
    return res.data
}