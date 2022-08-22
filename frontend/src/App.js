/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Button} from "@mui/material";
import React, {useEffect, useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";
import UserDetailsDialog from "./components/UserDetailsDialog";
import {createUser, updateUser} from "./services/searchService";
import {number} from "prop-types";

// import theme from "./Theme";

function App() {
    const theme = useTheme()
    const [cardIdCounter, setCardIdCounter] = useState(0)
    const [cards, setCards] = useState([])
    const [isUserDetailsDialogOpen, setIsUserDetailsDialogOpen] = useState(false)
    const [userId, setUserId] = useState(null)

    useEffect(() => {
        const newUserId = window.localStorage.getItem('user-id')
        setUserId(Number(newUserId))
    }, [])

    const handleNewSearchCard = () => {
        if(!userId){
            setIsUserDetailsDialogOpen(true)
            return
        }
        setCards([...cards, {id: cardIdCounter}])
        setCardIdCounter(cardIdCounter + 1)
    }
    const handleSearchCardDelete = (id) => {
        setCards(cards.filter(c => c.id !== id))
    }
    const handleNewUser = () => {
        setIsUserDetailsDialogOpen(true)
    }
    const handleCreateUser = async (values) => {
        const {id} = await createUser(values)
        setUserId(id)
        window.localStorage.setItem('user-id', id)
        handleUserDialogClose()
    }
    const handleUpdateUser = async (values) => {
        const statusCode = await updateUser({...values, id: userId})
        if (statusCode !== 204) {
            console.log('update user status', statusCode)
        }
        handleUserDialogClose()
    }
    const handleAccountFailure = () => {
        setIsUserDetailsDialogOpen(true)
        // TODO revoke other Linkedin searches that have been scheduled (need to lift state)
    }

    const handleUserDialogClose = () => {
        setIsUserDetailsDialogOpen(false)
        console.log('close')
    }

    return (
        <div
            // css={{backgroundColor: theme.palette.common.orange}}
        >
            <UserDetailsDialog
                isOpen={isUserDetailsDialogOpen}
                handleClose={handleUserDialogClose}
                handleSubmit={userId ? handleUpdateUser : handleCreateUser}
            />
            <h3 style={theme.typography.h3}>Blanket Application Strategy</h3>
            <h3 style={theme.typography.h4}>Tasks</h3>
            <div>
                <Button variant="outlined" onClick={handleNewUser}>New User</Button>
                <Button variant="outlined" onClick={handleNewSearchCard}>New Search</Button>

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
    );
}

export default App;
