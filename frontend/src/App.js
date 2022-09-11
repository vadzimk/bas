/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Alert, Button} from "@mui/material";
import React, {createContext, useEffect,} from 'react';
import {useTheme, css} from "@emotion/react";
import {useSelector, useDispatch} from "react-redux";
import {userLoggedIn} from "./reducers/userSlice";


import Tasks from "./components/Tasks";
import {Routes, Route, Link, useLocation} from "react-router-dom";
import Results from "./components/Results";
import Navigation from "./components/Navigation";

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
    console.log("location", pathname);

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
                <div css={{maxWidth: "1600px", margin: "0 auto"}}>
                    {notification.type &&
                    <Alert
                        severity={notification.type}
                        sx={{zIndex: "999999", position: "fixed", justifyContent: "center", width: "100%"}}>
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
                            justifyContent: "flex-end"
                        }}>
                            <h3 css={{...theme.typography.h4}}>
                                Blanket Application Strategy
                            </h3>
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
