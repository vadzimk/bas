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
import {addSearchCard, deleteSearchCard} from "./reducers/searchCardsSlice";
import {IndeedSearchCard} from "./components/IndeedSearchCard";


// import theme from "./Theme";


function App() {
    const theme = useTheme()
    const cards = useSelector(state => state.searchCards.cards)
    const user = useSelector(state => state.user)
    const notification = useSelector(state => state.notification)
    const dispatch = useDispatch();
    useEffect(() => {
        const user = JSON.parse(window.localStorage.getItem('bas-user')) // TODO persist the whole user object
        if (user?.id) {
            dispatch(userLoggedIn(user))
        }
    }, [])

    const handleNewSearchCardLinkedin = () => {
        if (!user.linkedin_credentials) {
            dispatch(notify({type: Ntypes.ERROR, message: 'Linkedin credentials are missing, please UPDATE USER'}))
            return
        }
        dispatch(addSearchCard('linkedin'))
    }

    const handleNewSearchCardIndeed = () => {
        // TODO not implemented
        dispatch(addSearchCard('indeed'))
    }

    const handleSearchCardDelete = (id) => {
        dispatch(deleteSearchCard(id))
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
                    onClick={handleNewSearchCardLinkedin}>
                    Linkedin Search
                </Button>}
                {user.id && <Button
                    variant="outlined"
                    onClick={handleNewSearchCardIndeed}>
                    Indeed Search
                </Button>}
            </div>
            <div>
                {user.id && cards.map(card =>
                    <Card
                        key={card.id}
                        cardId={card.id}
                        onDelete={() => handleSearchCardDelete(card.id)}
                        platform={card.jobBoard}
                    />
                )}
            </div>
        </div>
    )
}

function Card({platform, ...other}) {
    const platforms = {
        'linkedin': LinkedinSearchCard,
        'indeed': IndeedSearchCard,
    }
    const Component = platforms[platform]
    return <Component {...other}/>
}

export default App;
