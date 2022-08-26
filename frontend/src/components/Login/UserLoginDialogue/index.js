import React from 'react'
import Dialog from '@mui/material/Dialog';
import UserLoginForm from "./UserLoginForm";
import PropTypes from "prop-types";
import DialogTitle from "@mui/material/DialogTitle";
import {DialogContent} from "@mui/material";

UserLoginForm.propTypes = {
    handleSubmit: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired,
    isOpen: PropTypes.bool.isRequired,
}

export function UserLoginDialogue(props) {
    return (
        <div>
            <Dialog open={props.isOpen}>
                <DialogTitle>Login</DialogTitle>
                <DialogContent>
                    <UserLoginForm
                        {...props}
                    />
                </DialogContent>
            </Dialog>
        </div>
    )
}