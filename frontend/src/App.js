/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Alert, Button} from "@mui/material";
import React, {useEffect, useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";
import UserDetailsDialogue from "./components/UserDetailsDialogue";
import {createUser, updateUser} from "./services/searchService";
import {number} from "prop-types";
import {useSelector, useDispatch} from "react-redux";
import {loggedInAction, loginUser, registerUser, userLoggedIn} from "./reducers/userSlice";
import {UserLoginDialogue} from "./components/UserLoginDialogue";
import UserRegisterDialogue from "./components/UserRegisterDialogue";

// import theme from "./Theme";

function App() {
    const theme = useTheme()
    const [cardIdCounter, setCardIdCounter] = useState(0)
    const [cards, setCards] = useState([])
    const [isUserLoginOpen, setIsUserLoginOpen] = useState(false)
    const [isUserRegisterOpen, setIsUserRegisterOpen] = useState(false)
    const [isUserUpdateOpen, setIsUserUpdateOpen] = useState(false)

    // const [userId, setUserId] = useState(null)
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
    const handleCreateUser = async (values) => {
        // const {id} = await createUser(values)
        // setUserId(id)
        dispatch(registerUser(values)) // sends request
        console.log('hello from handleCreateUser')

        setIsUserRegisterOpen(false)
    }
    const handleUpdateUser = async (values) => {
        const statusCode = await updateUser({...values, id: userId})
        if (statusCode !== 204) {
            console.log('update user status', statusCode)
        }
        setIsUserUpdateOpen(false)
    }
    const handleAccountFailure = () => {
        setIsUserUpdateOpen(true)
        // TODO revoke other Linkedin searches that have been scheduled (need to lift state)
    }

    const handleLogin = (userFields) => {
        dispatch(loginUser(userFields))
    }

    const handleRegister = (userFields) => {
        dispatch(registerUser(userFields))
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
            <UserDetailsDialogue
                isOpen={isUserUpdateOpen}
                handleClose={() => setIsUserUpdateOpen(false)}
                handleSubmit={userId ? handleUpdateUser : handleCreateUser}
            />
            <UserLoginDialogue
                isOpen={isUserLoginOpen}
                handleSubmit={handleLogin}
                handleClose={() => setIsUserLoginOpen(false)}
            />
            <UserRegisterDialogue
                isOpen={isUserRegisterOpen}
                handleSubmit={handleRegister}
                handleClose={() => setIsUserRegisterOpen(false)}
            />

            <h3 style={theme.typography.h3}>Blanket Application Strategy</h3>
            <h3 style={theme.typography.h4}>Tasks</h3>
            <div style={{display: 'flex'}}>
                {userId ?
                    <div>
                        <Button
                            variant="outlined"
                            onClick={() => setIsUserUpdateOpen(true)}
                        >
                            Update User
                        </Button>
                        <Button
                            variant="outlined"
                            onClick={handleNewSearchCard}>
                            New Search
                        </Button>
                    </div>
                    :
                    <div>
                        <Button
                            variant="outlined"
                            onClick={() => setIsUserRegisterOpen(true)}
                        >
                            New User
                        </Button>
                        <Button
                            variant="outlined"
                            onClick={() => setIsUserUpdateOpen(true)}
                        >
                            Existing User
                        </Button>
                    </div>
                }
            </div>
            <div>
                {cards.map(card =>
                    <LinkedinSearchCard
                        key={card.id}
                        onDelete={() => handleSearchCardDelete(card.id)}
                        userId={userId}
                        handleAccountFailure={handleAccountFailure}
                    />
                )}
            </div>
        </div>
    )
}

export default App;
