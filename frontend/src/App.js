/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import React, {createContext, useEffect,} from 'react';
import {useTheme, css} from "@emotion/react";
import {useSelector, useDispatch} from "react-redux";
import {userLoggedIn} from "./reducers/userSlice";


import Tasks from "./components/Tasks";
import {Routes, Route, Link, useLocation} from "react-router-dom";
import Results from "./components/Results";
import Navigation from "./components/Navigation";

import {Alert, AlertIcon, Text} from '@chakra-ui/react'

// import theme from "./Theme";

export const SearchCardContext = createContext({
    cardId: null,
    onDelete: null,
    platform: null
})

function App() {
    const theme = useTheme()
    const user = useSelector(state => state.user)
    const notification = useSelector(state => state.notification)
    const dispatch = useDispatch();
    const {pathname} = useLocation();

    useEffect(() => {
        const user = JSON.parse(window.localStorage.getItem('bas-user')) // TODO persist the whole user object
        if (user?.id) {
            dispatch(userLoggedIn(user))
        }
    }, [])


    return (
        <div style={{position: "relative"}}>
            <div css={{height: "100px", backgroundColor: theme.palette.common.blue1}}/>
            <div style={{position: "absolute", top: 0, left: 0, width: "100%"}}>
                <div css={{maxWidth: "1600px", margin: "0 auto", display: "flex", flexDirection: "column"}}>
                    {notification.type &&
                    <Alert
                        status={notification.type}
                        style={{zIndex: "999999", position: "fixed", justifyContent: "center", alignSelf: "center"}}
                    >
                        <AlertIcon/>
                        {notification.message}
                    </Alert>
                    }
                    <div css={{
                        display: 'flex', justifyContent: 'space-between'
                    }}>
                        <div style={{
                            height: "100px",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "flex-end",
                        }}>
                            <Text fontSize="4xl" >
                                Blanket Application Strategy
                            </Text>
                        </div>
                        <div style={{
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'flex-end',
                        }}>
                            <Navigation user={user} pathname={pathname}/>
                        </div>
                    </div>
                </div>
                <Routes>
                    <Route path="/" element={<Tasks/>}/>
                    <Route path="/task-results" element={<Results/>}/>
                </Routes>
            </div>
        </div>
    )
}


export default App;
