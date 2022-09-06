import React, {useState} from 'react'
import {Button} from "@mui/material";
import {useDispatch, useSelector} from "react-redux";
import UserDetailsDialogue from "./UserDetailsDialogue";
import {updateUser} from "../../reducers/userSlice";

export default function Profile() {
    const [isUserUpdateOpen, setIsUserUpdateOpen] = useState(false)
    const userId = useSelector(state => state.user.id)
    const dispatch = useDispatch()
    const handleUpdateUser = async (values) => {
        dispatch(updateUser({...values, id: userId}))
        setIsUserUpdateOpen(false)
    }
    return (
        <div style={{flexShrink:0}}>
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