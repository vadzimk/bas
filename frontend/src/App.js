/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Button} from "@mui/material";
import React, {useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";

function App() {
    // const theme = useTheme()
    const [idCounter, setIdCounter] = useState(0)
    const [searchCards, setSearchCards] = useState([])
    const handleClick = () => {
        setSearchCards([...searchCards, {id: idCounter}])
        setIdCounter(idCounter+1)
    }
    const handleDelete = (id) => {
        setSearchCards(searchCards.filter(c => c.id !== id))
    }


    return (
        <div
            // css={{backgroundColor: theme.palette.common.orange}}
        >
            <Button variant="outlined" onClick={handleClick}>New Search</Button>
            <div>
                {searchCards.map(card =>
                    <LinkedinSearchCard key={card.id} onDelete={() => handleDelete(card.id)}/>
                )}
            </div>
        </div>
    );
}

export default App;
