// using the confitureStore api
import {configureStore} from '@reduxjs/toolkit';
import userReducer from './reducers/userSlice'
import notificationReducer from "./reducers/notificationSlice";
import tasksReducer from './reducers/tasksSlice'


export const store = configureStore({
    reducer: {
        user: userReducer,
        notification: notificationReducer,
        tasks: tasksReducer
    }
})