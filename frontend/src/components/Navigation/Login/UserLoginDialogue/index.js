import React from 'react'
import UserLoginForm from "./UserLoginForm";
import PropTypes from "prop-types";

import {ModalOverlay, Modal, ModalHeader, ModalContent} from "@chakra-ui/react"

UserLoginDialogue.propTypes = {
    handleSubmit: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired,
    isOpen: PropTypes.bool.isRequired,
}

export function UserLoginDialogue(props) {
    return (
        <div>
            <Modal isOpen={props.isOpen}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Login</ModalHeader>
                        <UserLoginForm
                            {...props}
                        />
                </ModalContent>
            </Modal>
        </div>
    )
}