import React from 'react'
import {Button} from "@mui/material";
import {useDispatch} from "react-redux";
import {userLogout} from "../../reducers/userSlice";
import {clearNotification} from "../../reducers/notificationSlice";

export default function Logout() {
    const dispatch = useDispatch()

    const handleLogout = () => {
        dispatch(userLogout())
        dispatch(clearNotification())
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