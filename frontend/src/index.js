import React from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
import {BrowserRouter as Router} from 'react-router-dom'
import {ThemeProvider as MuiThemeProvider} from "@mui/material";
import {ThemeProvider as EmotionThemeProvider} from "@emotion/react";
import theme from './Theme'
import {Provider} from "react-redux";
import {store} from "./store";
import {PersistGate} from 'redux-persist/integration/react'
import {persistStore} from 'redux-persist'

let persistor =persistStore(store)
const root = createRoot(document.getElementById('root'))

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                <MuiThemeProvider theme={theme}>
                    <EmotionThemeProvider theme={theme}>
                        <Router>
                            <App/>
                        </Router>
                    </EmotionThemeProvider>
                </MuiThemeProvider>
            </PersistGate>
        </Provider>
    </React.StrictMode>
)