/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Alert, Button} from "@mui/material";
import React, {useEffect, useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";
import {useSelector, useDispatch} from "react-redux";
import {loginUser, userLoggedIn} from "./reducers/userSlice";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Login from "./components/Login";
import Logout from "./components/Logout";
import {notify, Ntypes} from "./reducers/notificationSlice";


// import theme from "./Theme";

function App() {
    const theme = useTheme()
    const [cardIdCounter, setCardIdCounter] = useState(0)
    const [cards, setCards] = useState([])
    const user = useSelector(state => state.user)
    const notification = useSelector(state => state.notification)
    const dispatch = useDispatch();
    useEffect(() => {
        const userId = window.localStorage.getItem('user-id')
        if (userId) {
            dispatch(userLoggedIn(userId))
        }
    }, [])

    const handleNewSearchCard = () => {
        if (!user.hasLinkedinCredentials) {
            dispatch(notify({type: Ntypes.ERROR, message: 'Linkedin credentials are missing, please UPDATE USER'}))
            return
        }
        setCards([...cards, {id: cardIdCounter}])
        setCardIdCounter(cardIdCounter + 1)
    }
    const handleSearchCardDelete = (id) => {
        setCards(cards.filter(c => c.id !== id))
    }
    return (
        <div
            // css={{backgroundColor: theme.palette.common.orange}}
        >
            {notification.type &&
            <Alert
                severity={notification.type}
                sx={{zIndex: "999999", position: "fixed", justifyContent: "center", width: "100%"}}
            >
                {notification.message}
            </Alert>
            }

            <div css={{display: 'flex', justifyContent: 'space-between', backgroundColor: theme.palette.common.blue1}}>
                <div style={{height: "100px", display: "flex", flexDirection: "column", justifyContent: "flex-end"}}>
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
            <h3 style={theme.typography.h4}>Tasks</h3>
            <div style={{display: 'flex'}}>

                {user.id && <Button
                    variant="outlined"
                    onClick={handleNewSearchCard}>
                    New Search
                </Button>}
            </div>
            <div>
                {user.id && cards.map(card =>
                    <LinkedinSearchCard
                        key={card.id}
                        onDelete={() => handleSearchCardDelete(card.id)}
                    />
                )}
            </div>
        </div>
    )
}

export default App;
