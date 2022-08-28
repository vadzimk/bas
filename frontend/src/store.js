// using the confitureStore api
import {configureStore} from '@reduxjs/toolkit';
import userReducer from './reducers/userSlice'
import notificationReducer from "./reducers/notificationSlice";
import searchCardsReducer from './reducers/searchCardsSlice'


export const store = configureStore({
    reducer: {
        user: userReducer,
        notification: notificationReducer,
        searchCards: searchCardsReducer
    }
})