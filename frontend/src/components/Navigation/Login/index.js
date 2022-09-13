import React, {useState} from 'react'
import {loginUser} from "../../../reducers/userSlice";
import {useDispatch} from "react-redux";
import {UserLoginDialogue} from "./UserLoginDialogue";

import {Button} from "@chakra-ui/react"

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
                variant="outline"
                onClick={() => setIsUserLoginOpen(true)}
            >
                Existing User
            </Button>
        </div>

    )
}