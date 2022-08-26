import {createAsyncThunk, createSlice} from '@reduxjs/toolkit'
import {authUser, createUser} from "../services/searchService";
import {notify, Ntypes} from "./notificationSlice";

const initialState = {
    id: null,
    status: 'idle', //  idle, loading, succeeded, failed TODO do i need this?
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        userLoggedIn: function (state, action) {
            state.id = action.payload
            console.log('hello from userLoggedIn')
        },
        userLogout: function (state, action){
            state.id = null
            window.localStorage.removeItem('user-id')
        }
        // userRegistered: function (state, action) {
        //     state.id = action.payload
        //     console.log('hello from userRegistered')
        // }
    },
    extraReducers: builder => {
        builder.addCase(registerUser.fulfilled, (state, action) => {
            if(!action.payload){
                return
            }
            state.id = action.payload
            window.localStorage.setItem('user-id', action.payload)
            console.log('hello form .addCase(registerUser.fulfilled)')

        })
            .addCase(registerUser.rejected, (state, action) => {
                state.error = action.payload.error
                console.log('registerUser.rejected', action.payload.error)
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.id = action.payload
                window.localStorage.setItem('user-id', action.payload)
                console.log('hello from .addCase(loginUser.fulfilled)')
            })

    }
})

export const loginUser = createAsyncThunk('user/login', async (userFields) => {
    // userFields = {username}
    const data = await authUser(userFields)
    return data.id
})

export const registerUser = createAsyncThunk('user/register', async (userFields, {dispatch}) => {
    const data = await createUser(userFields)
    if (data.error) {
        dispatch(notify({message: data.error, type: Ntypes.ERROR}))
        return
    }
    return data.id
})

export const {userLoggedIn, userRegistered, userLogout} = userSlice.actions // action creators return action objects of the shape {type: 'auto-generated-id}, abstracts the case statements in redux-core
export default userSlice.reducer
