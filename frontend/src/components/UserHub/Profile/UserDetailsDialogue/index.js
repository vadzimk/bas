import * as React from 'react';

import UserDetailsForm from "./UserDetailsForm";
import PropTypes from "prop-types";
import {ModalOverlay, Modal, ModalHeader, ModalContent, ModalBody, Text, Link} from "@chakra-ui/react"
import { ExternalLinkIcon } from '@chakra-ui/icons'

UserDetailsDialogue.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
}

export default function UserDetailsDialogue({isOpen, ...other}) {
    const title = "Update Account"
    const content = <>
        <Text>
            Generate Email on
            <Link isExternal href="https://www.1secmail.com/" target="_blank" rel="noreferrer"> 1secmail<ExternalLinkIcon mx='2px'/> </Link> or <Link isExternal href="https://tempmail.ninja" target="_blank" rel="noreferrer"> tempmail<ExternalLinkIcon mx='2px'/></Link>
            <span> And enter mock <a href="https://www.linkedin.com/signup/" target="_blank" rel="noreferrer">Linkedin</a> credentials to scrape it. </span>
        </Text>
        <Text>
            <span>First name: </span><span><b>Baton</b></span>
        </Text>
        <Text>
            <span>Last name: </span><span><b>Crusader</b></span>
        </Text>
    </>

    return (
        <div>
            <Modal isOpen={isOpen}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>{title}</ModalHeader>
                <ModalBody>
                    {content}
                    <UserDetailsForm
                        {...other}
                    />
                </ModalBody>
                </ModalContent>
            </Modal>
        </div>
    );
}
