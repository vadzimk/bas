import React, {useState} from 'react'
import {Button} from "@mui/material";
import {loginUser} from "../../reducers/userSlice";
import {useDispatch} from "react-redux";
import {UserLoginDialogue} from "./UserLoginDialogue";

export default function Login() {
    const [isUserLoginOpen, setIsUserLoginOpen] = useState(false)
    const dispatch = useDispatch();

    const handleLogin = (userFields) => {
        dispatch(loginUser(userFields))
    }

    return (
        <div>
            <UserLoginDialogue
                isOpen={isUserLoginOpen}
                handleSubmit={handleLogin}
                handleClose={() => setIsUserLoginOpen(false)}
            />
            <Button
                variant="outlined"
                onClick={() => setIsUserLoginOpen(true)}
            >
                Existing User
            </Button>
        </div>

    )
}