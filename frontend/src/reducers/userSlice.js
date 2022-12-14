import {createAsyncThunk, createSlice} from '@reduxjs/toolkit'
import {notify, notifyTemp, Ntypes} from "./notificationSlice";
import api from "../services/api";

const initialState = {
    id: null,
    status: 'idle', //  idle, loading, succeeded, failed TODO do i need this?
    linkedin_credentials: false,
    login_verification_request: null,
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        userLoggedIn: function (state, action) {
            return {...state, ...action.payload}  // replace state entirely
        },
        userLogout: function (state, action) {
            window.localStorage.removeItem('bas-user')
            return initialState
        },
        loginVerificationRequested(state, action){
            // action.payload: {task_id, email}
            state.login_verification_request = action.payload
        }
        // userRegistered: function (state, action) {
        //     state.id = action.payload
        //     console.log('hello from userRegistered')
        // }
    },
    extraReducers: builder => {
        builder.addCase(registerUser.fulfilled, (state, action) => {
            const {id} = action.payload
            state.id = id
        })
            .addCase(loginUser.fulfilled, (state, action) => {
                const {id, linkedin_credentials} = action.payload
                state.id = id
                state.linkedin_credentials = linkedin_credentials
            })
            .addCase(updateUser.fulfilled, (state, action) => {
                const {id, linkedin_credentials} = action.payload
                state.id = id
                state.linkedin_credentials = linkedin_credentials
            })
            .addCase(verifyPin.fulfilled, (state, action)=>{
                state.login_verification_request = null
            })
    }
})

export const loginUser = createAsyncThunk('user/login', async (userFields, {dispatch, rejectWithValue}) => {
    // @param userFields: {username}
    console.log('will do auth')
    try {
        const res = await api.post('/user/login', {...userFields})
        dispatch(notifyTemp({type: Ntypes.SUCCESS, message: `Hi, ${userFields.username}`}))
        window.localStorage.setItem('bas-user', JSON.stringify(res.data))
        return res.data // data = {id, linkedin_credentials}
    } catch (e) {
        if (e.response.status === 404) {
            dispatch(notifyTemp({type: Ntypes.ERROR, message: `Not found "${userFields.username}"`}))
        } else {
            dispatch(notifyTemp({type: Ntypes.ERROR, message: e.message}))
        }
        rejectWithValue(e.response.json())
    }
})

export const registerUser = createAsyncThunk('user/register', async (userFields, {dispatch, rejectWithValue}) => {
    // @param userFields: {linkedin_email, linkedin_password}
    try {
        const res = await api.post('/user', {...userFields})
        window.localStorage.setItem('bas-user', JSON.stringify(res.data))
        return res.data
    } catch (e) {
        const message = e.response.data ? e.response.data : e.message
        dispatch(notify({message: message, type: Ntypes.ERROR}))
        rejectWithValue(e.response.json())
    }
})

export const updateUser = createAsyncThunk('user/update', async (userFields, {dispatch, rejectWithValue}) => {
    // @param userFields: {id, linkedin_email, linkedin_password}
    try {
        const res = await api.put('/user', {...userFields})
        dispatch(notifyTemp({type: Ntypes.SUCCESS, message: 'OK'}))
        return res.data
    } catch (e) {
        const message = e.response.data ? e.response.data : e.message
        dispatch(notifyTemp({type: Ntypes.ERROR, message}))
        rejectWithValue(e.response.json())
    }

})

export const verifyPin = createAsyncThunk('user/handleVerifyPin', async({pin, task_id}, {dispatch, rejectWithValue})=>{
        try {
        const res = await api.post('/verification', {pin, task_id})
        dispatch(notifyTemp({type: Ntypes.SUCCESS, message: res.data}))
        return res.data
    } catch (e) {
        const message = e.response.data ? e.response.data : e.message
        dispatch(notifyTemp({type: Ntypes.ERROR, message}))
        rejectWithValue(e.response.json())
    }
})

export const {userLoggedIn, loginVerificationRequested, userLogout} = userSlice.actions // action creators return action objects of the shape {type: 'auto-generated-id}, abstracts the case statements in redux-core
export default userSlice
