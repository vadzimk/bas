import {createAsyncThunk} from "@reduxjs/toolkit";

const {createSlice} = require("@reduxjs/toolkit");
export const Ntypes = Object.freeze({
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
    SUCCESS: 'success'
})

const initialState = { // one of Ntypes
    message: '',
    type: null,
}

const notificationSlice = createSlice({
    name: 'notification',
    initialState,
    reducers: {
        notify: function (state, action) {
            state.message = action.payload.message;
            state.type = action.payload.type;
            console.log('notification: ', action.payload.message)
        },
        clearNotification: function (state, action) {
            state.message = '';
            state.type = null
        }
    }
})

const sleep = (ms)=>new Promise(resolve => {setTimeout(()=>resolve(), ms)})

export const notifyTemp = createAsyncThunk('notification/timed', async (conf, {dispatch})=>{
    // notification with timeout
    // conf = {type: Ntypes, message, timeout: sec }
    const {timeout, ...notification} = conf
    const ms = timeout ? timeout * 1000 : 5000
    dispatch(notify(notification))
    await sleep(ms)
    dispatch(notify({type: null, message: ''}))
})

export const {notify, clearNotification} = notificationSlice.actions
export default notificationSlice.reducer