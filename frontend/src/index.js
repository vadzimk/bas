import React from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
import {ThemeProvider as MuiThemeProvider} from "@mui/material";
// import {ThemeProvider as EmotionThemeProvider} from "@emotion/react";
import {themeMui} from './ThemeMui'
import {Provider} from "react-redux";
import {store} from "./store";
import {PersistGate} from 'redux-persist/integration/react'
import {persistStore} from 'redux-persist'

import {ChakraProvider} from '@chakra-ui/react'
import {themeChakra} from "./ThemeChakra";

let persistor = persistStore(store)
const root = createRoot(document.getElementById('root'))

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                    <MuiThemeProvider theme={themeMui}>
                <ChakraProvider theme={themeChakra} resetCSS={true}>
                        {/*<EmotionThemeProvider theme={themeMui}>*/}
                            <App/>
                        {/*</EmotionThemeProvider>*/}
                </ChakraProvider>
                    </MuiThemeProvider>
            </PersistGate>
        </Provider>
    </React.StrictMode>
)