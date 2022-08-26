import React, {useState} from 'react'
import {Button} from "@mui/material";
import {updateUser} from "../../services/searchService";
import {useSelector} from "react-redux";
import UserDetailsDialogue from "./UserDetailsDialogue";

export default function Profile() {
    const [isUserUpdateOpen, setIsUserUpdateOpen] = useState(false)
    const userId = useSelector(state => state.user.id)

    const handleUpdateUser = async (values) => {
        const statusCode = await updateUser({...values, id: userId})
        if (statusCode !== 204) {
            console.log('update user status', statusCode)
        }
        setIsUserUpdateOpen(false)
    }
    return (
        <div>
            <UserDetailsDialogue
                isOpen={isUserUpdateOpen}
                handleClose={() => setIsUserUpdateOpen(false)}
                handleSubmit={handleUpdateUser}
            />
            <Button
                variant="outlined"
                onClick={() => setIsUserUpdateOpen(true)}
            >
                Update User
            </Button>
        </div>
    )
}