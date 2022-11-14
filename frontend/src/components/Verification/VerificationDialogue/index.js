import React from 'react'
import PropTypes from "prop-types";

import {ModalOverlay, Modal, ModalHeader, ModalContent} from "@chakra-ui/react"
import VerificationDialogueForm from "./VerificationDialogueForm";

VerificationDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired,
}

export function VerificationDialogue(props) {
    return (
        <div>
            <Modal isOpen={props.isOpen}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Enter PIN from email</ModalHeader>
                        <VerificationDialogueForm
                            {...props}
                        />
                </ModalContent>
            </Modal>
        </div>
    )
}