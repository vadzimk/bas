/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Button} from "@mui/material";
import React, {useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";
import LinkedinLogin from "./components/LinkedinLogin";
// import theme from "./Theme";

function App() {
    const theme = useTheme()
    const [idCounter, setIdCounter] = useState(0)
    const [searchCards, setSearchCards] = useState([])
    const [isLinkedinLoginOpen, setIsLinkedinLoginOpen] = useState(false)
    const handleNewSearchCard = () => {
        setSearchCards([...searchCards, {id: idCounter}])
        setIdCounter(idCounter+1)
    }
    const handleSearchCardDelete = (id) => {
        setSearchCards(searchCards.filter(c => c.id !== id))
    }

    //    TODO connect a modal where to enter a new email address for linkedin account when it is blocked
    return (
        <div
            // css={{backgroundColor: theme.palette.common.orange}}
        >
            <LinkedinLogin isOpen={isLinkedinLoginOpen}/>
            <h3 style={theme.typography.h3}>Blanket Application Strategy</h3>
            <Button variant="outlined" onClick={handleNewSearchCard}>New Search</Button>
            <div>
                {searchCards.map(card =>
                    <LinkedinSearchCard key={card.id} onDelete={() => handleSearchCardDelete(card.id)}/>
                )}
            </div>
        </div>
    );
}

export default App;
