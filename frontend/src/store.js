// using the confitureStore api
import {configureStore} from '@reduxjs/toolkit';
import userReducer from './reducers/userSlice'
import notificationReducer from "./reducers/notificationSlice";
import searchCardsReducer from './reducers/searchCardsSlice'
import {combineReducers} from 'redux';
import {persistReducer} from 'redux-persist'
import thunk from 'redux-thunk'
import storage from 'redux-persist/lib/storage'

// using redux-persist example from https://codesandbox.io/s/izxb6?file=/src/app/store.js
const reducers = combineReducers({
        user: userReducer,
        notification: notificationReducer,
        searchCards: searchCardsReducer
})

const persistConfig = {
    key: 'root',
    storage
}

const persistedReducer = persistReducer(persistConfig, reducers)

export const store = configureStore({
    reducer: persistedReducer,
    devTools: process.env.NODE_ENV !== 'production',
    middleware: [thunk]
})