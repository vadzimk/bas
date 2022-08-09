import React from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
import {BrowserRouter as Router} from 'react-router-dom'
import {ThemeProvider as MuiThemeProvider} from "@mui/material";
import {ThemeProvider as EmotionThemeProvider} from "@emotion/react";
import theme from './Theme'

const root = createRoot(document.getElementById('root'))

root.render(
    <MuiThemeProvider theme={theme}>
        <EmotionThemeProvider theme={theme}>
            <Router>
                <App/>
            </Router>
        </EmotionThemeProvider>
    </MuiThemeProvider>
)