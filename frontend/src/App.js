/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import {Button} from "@mui/material";
import React, {useState} from 'react';
import {useTheme, css} from "@emotion/react";
import LinkedinSearchCard from "./components/LinkedinSearchCard";

function App() {
    // const theme = useTheme()
    const [searchCards, setSearchCards] = useState([])
    const handleClick = () => {
        setSearchCards([...searchCards, LinkedinSearchCard])
    }


    return (
        <div
            // css={{backgroundColor: theme.palette.common.orange}}
        >
            <Button variant="outlined" onClick={handleClick}>New Search</Button>
            <div>{searchCards.map((Card, index) => <Card key={index}/>)}</div>
        </div>
    );
}

export default App;
