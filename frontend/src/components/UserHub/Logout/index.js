import React from 'react'
import {Button} from "@chakra-ui/react";
import {useDispatch} from "react-redux";
import {userLogout} from "../../../reducers/userSlice";
import {clearNotification} from "../../../reducers/notificationSlice";

export default function Logout() {
    const dispatch = useDispatch()

    const handleLogout = () => {
        dispatch(userLogout())
        dispatch(clearNotification())
    }
    return (
        <div>
            <Button
                onClick={handleLogout}
            >
                Exit
            </Button>
        </div>
    )
}