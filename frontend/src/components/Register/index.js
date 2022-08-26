import React, {useState} from 'react'
import {registerUser} from "../../reducers/userSlice";
import {Button} from "@mui/material";
import UserRegisterDialogue from "./UserRegisterDialogue";
import {useDispatch, useSelector} from "react-redux";
import {clearNotification} from "../../reducers/notificationSlice";

export default function Register() {

    const [isUserRegisterOpen, setIsUserRegisterOpen] = useState(false)
    const userId = useSelector(state => state.user.id)
    const dispatch = useDispatch();


    const handleRegister = (userFields) => {
        dispatch(registerUser(userFields))
        if (userId) {
            setIsUserRegisterOpen(false)
        }
    }
    const handleNewUserClick = () => {
        setIsUserRegisterOpen(true)
        dispatch(clearNotification())
    }
    const handleCancelClick = () => {
        setIsUserRegisterOpen(false)
        dispatch(clearNotification())
    }

    return (
        <div>

            <UserRegisterDialogue
                isOpen={isUserRegisterOpen}
                handleSubmit={handleRegister}
                handleClose={handleCancelClick}
            />
            <Button
                variant="outlined"
                onClick={handleNewUserClick}
            >
                New User
            </Button>
        </div>
    )
}