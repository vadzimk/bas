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

export const {notify, clearNotification} = notificationSlice.actions
export default notificationSlice.reducer