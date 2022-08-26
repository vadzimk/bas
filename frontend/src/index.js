import React from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
import {BrowserRouter as Router} from 'react-router-dom'
import {ThemeProvider as MuiThemeProvider} from "@mui/material";
import {ThemeProvider as EmotionThemeProvider} from "@emotion/react";
import theme from './Theme'
import {Provider} from "react-redux";
import {store} from "./store";

const root = createRoot(document.getElementById('root'))

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <MuiThemeProvider theme={theme}>
                <EmotionThemeProvider theme={theme}>
                    <Router>
                        <App/>
                    </Router>
                </EmotionThemeProvider>
            </MuiThemeProvider>
        </Provider>
    </React.StrictMode>
)