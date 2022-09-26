// using the confitureStore api
import {configureStore} from '@reduxjs/toolkit';
import {combineReducers} from 'redux';
import {persistReducer} from 'redux-persist'
import thunk from 'redux-thunk'
import storage from 'redux-persist/lib/storage'
import userSlice from "./reducers/userSlice";
import notificationSlice from "./reducers/notificationSlice";
import searchCardsSlice from "./reducers/searchCardsSlice";
import resultsSlice from "./reducers/resultsSlice";

// using redux-persist example from https://codesandbox.io/s/izxb6?file=/src/app/store.js
const reducers = combineReducers({
        user: userSlice.reducer,
        notification: notificationSlice.reducer,
        searchCards: searchCardsSlice.reducer,
        results: resultsSlice.reducer,
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