import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import UserDetailsForm from "./UserDetailsForm";
import PropTypes from "prop-types";

UserDetailsDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
}

export default function UserDetailsDialogue({isOpen, ...other}) {
    const title = "Update Account"
    const content = <>
        <DialogContentText>
            <a href="https://www.1secmail.com/" target="_blank" rel="noreferrer">Generate Email</a>
            <span> And enter fake <a href="https://www.linkedin.com/signup/" target="_blank" rel="noreferrer">Linkedin</a> credentials to scrape it. </span>
        </DialogContentText>
        <DialogContentText>
            <span>First name: </span><span><b>Baton</b></span>
        </DialogContentText>
        <DialogContentText>
            <span>Last name: </span><span><b>Crusader</b></span>
        </DialogContentText>
    </>

    return (
        <div>
            <Dialog open={isOpen}>
                <DialogTitle>{title}</DialogTitle>
                <DialogContent>
                    {content}
                    <UserDetailsForm
                        {...other}
                    />
                </DialogContent>
            </Dialog>
        </div>
    );
}
