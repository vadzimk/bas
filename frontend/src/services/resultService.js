import api from "./api";

export const getAllResults = async () => {
    const res = await api.get('/jobs')
    return res.data
}

// api.get('/jobs').then((res) => {
//     table.setData(res.data)
//     // restoreColumnLayout()
// }).catch((err) => console.log(err))