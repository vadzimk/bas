import api from "./api";

export const editUser = async (userFields) => {
    // @param userFields: {id, linkedin_email, linkedin_password}
    const res = await api.put('/user', {...userFields})
    return res.status
}

export const createUser = async (userFields)=>{
        // @param userFields: {linkedin_email, linkedin_password}
    const res= await api.post('/user', {...userFields})
    return res.data
}

export const authUser = async(userFields)=>{
    // @param userFields: {username}
    const res= await api.post('/user/login', {...userFields})
    return res.data
}