import React from 'react'
import {Button} from "@mui/material";
import {useDispatch} from "react-redux";
import {userLogout} from "../../reducers/userSlice";

export default function Logout() {
    const dispatch = useDispatch()

    const handleLogout = () => {
        dispatch(userLogout())
    }
    return (
        <div>
            <Button
                variant="outlined"
                onClick={handleLogout}
            >
                Exit
            </Button>
        </div>
    )
}