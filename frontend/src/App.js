/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Alert} from "@mui/material";
import React, {createContext, useEffect,} from 'react';
import {useTheme, css} from "@emotion/react";
import {useSelector, useDispatch} from "react-redux";
import {userLoggedIn} from "./reducers/userSlice";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Login from "./components/Login";
import Logout from "./components/Logout";

import Tasks from "./components/Tasks";


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
    useEffect(() => {
        const user = JSON.parse(window.localStorage.getItem('bas-user')) // TODO persist the whole user object
        if (user?.id) {
            dispatch(userLoggedIn(user))
        }
    }, [])


    return (
        <div style={{position: "relative"}}>
            <div css={{height: "100px", backgroundColor: theme.palette.common.blue1}}></div>
            <div style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
            }}>
                <div
                    css={{
                        maxWidth: "1600px",
                        margin: "0 auto",

                    }}
                >
                    {notification.type &&
                    <Alert
                        severity={notification.type}
                        sx={{zIndex: "999999", position: "fixed", justifyContent: "center", width: "100%"}}
                    >
                        {notification.message}
                    </Alert>
                    }

                    <div css={{
                        display: 'flex',
                        justifyContent: 'space-between',

                    }}>
                        <div style={{
                            height: "100px",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "flex-end",
                        }}>
                            <h3 css={{...theme.typography.h3}}>
                                Blanket Application Strategy
                            </h3>
                        </div>
                        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'flex-end'}}>
                            <div style={{display: 'flex',}}>
                                {user.id ?
                                    <>
                                        <Profile/>
                                        <Logout/>
                                    </>
                                    :
                                    <>
                                        <Register/>
                                        <Login/>
                                    </>
                                }
                            </div>
                        </div>
                    </div>
                </div>


                    <Tasks/>
                </div>
        </div>
    )
}


export default App;
