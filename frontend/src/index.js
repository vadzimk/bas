import React from 'react'
import {createRoot} from 'react-dom/client'
import App from './App'
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
                <ChakraProvider theme={themeChakra} resetCSS={true}>
                            <App/>
                </ChakraProvider>
            </PersistGate>
        </Provider>
    </React.StrictMode>
)