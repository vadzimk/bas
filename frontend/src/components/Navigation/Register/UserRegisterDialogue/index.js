import React from 'react'
import PropTypes from "prop-types";
import UserLoginForm from "../../Login/UserLoginDialogue/UserLoginForm";
import {ModalOverlay, Modal, ModalHeader, ModalContent} from "@chakra-ui/react"

UserRegisterDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired
}

export default function UserRegisterDialogue(props) {

    return (
        <Modal isOpen={props.isOpen}>
            <ModalOverlay />
            <ModalContent>
                    <ModalHeader>
                New User
                    </ModalHeader>

                <UserLoginForm
                    {...props}
                />
            </ModalContent>
        </Modal>
    )
}