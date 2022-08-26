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


// import theme from "./Theme";

function App() {
    const theme = useTheme()
    const [cardIdCounter, setCardIdCounter] = useState(0)
    const [cards, setCards] = useState([])
    const userId = useSelector(state => state.user.id)
    const notification = useSelector(state => state.notification)
    const dispatch = useDispatch();
    useEffect(() => {
        const userId = window.localStorage.getItem('user-id')
        if (userId) {
            dispatch(userLoggedIn(userId))
        }
    }, [])

    const handleNewSearchCard = () => {
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
                sx={{zIndex: "999999", position: "relative"}}
            >
                {notification.message}
            </Alert>
            }

            <div css={{display: 'flex', justifyContent: 'space-between', backgroundColor: theme.palette.common.blue1}}>
                <div>
                    <h3 style={theme.typography.h3}>Blanket Application Strategy</h3>
                </div>
                <div style={{display: 'flex'}}>
                    {userId ?
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
            <h3 style={theme.typography.h4}>Tasks</h3>
            <div style={{display: 'flex'}}>

                {userId && <Button
                    variant="outlined"
                    onClick={handleNewSearchCard}>
                    New Search
                </Button>}
            </div>
            <div>
                {cards.map(card =>
                    <LinkedinSearchCard
                        key={card.id}
                        onDelete={() => handleSearchCardDelete(card.id)}
                        userId={userId}
                    />
                )}
            </div>
        </div>
    )
}

export default App;
