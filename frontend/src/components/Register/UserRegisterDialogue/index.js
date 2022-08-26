import React from 'react'
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import PropTypes from "prop-types";
import UserLoginForm from "../../Login/UserLoginDialogue/UserLoginForm";
import {DialogContent} from "@mui/material";

UserRegisterDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired
}

export default function UserRegisterDialogue(props) {

    return (
        <Dialog open={props.isOpen}>
            <DialogTitle>
                New User
            </DialogTitle>
            <DialogContent>
                <UserLoginForm
                    {...props}
                />
            </DialogContent>
        </Dialog>
    )
}