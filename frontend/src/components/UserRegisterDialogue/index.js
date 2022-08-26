import React from 'react'
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import UserLoginForm from "../UserLoginDialogue/UserLoginForm";
import PropTypes from "prop-types";

UserRegisterDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired
}

export default function UserRegisterDialogue(props){

    return (
        <Dialog open={props.isOpen}>
            <DialogTitle>
                New User
            </DialogTitle>
            <UserLoginForm
                {...props}
            />
        </Dialog>
    )
}