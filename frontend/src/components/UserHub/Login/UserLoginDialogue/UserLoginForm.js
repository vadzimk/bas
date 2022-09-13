import React from 'react'
import {Formik} from "formik";
import PropTypes from "prop-types";
import {ModalBody, FormLabel, ModalFooter, Button, Input} from "@chakra-ui/react"

UserLoginForm.propTypes = {
    handleSubmit: PropTypes.func.isRequired,
    handleClose: PropTypes.func.isRequired,
}
export default function UserLoginForm({handleSubmit, handleClose}) {
    let initialValues = {
        username: 'unnamed'
    };

    const validate = (values) => {
        const errors = {};
        if (!values.username) {
            errors.username = 'Required'
        }
        return errors
    }

    return (
        <Formik
            initialValues={initialValues}
            validate={validate}
            onSubmit={handleSubmit}>
            {(formikProps) => (
                <form onSubmit={formikProps.handleSubmit}>
                    <ModalBody>
                        <FormLabel>Username</FormLabel>
                        <Input
                            // margin="dense"
                            // label="Username"
                            // fullWidth
                            name="username"
                            variant="outline"
                            onChange={formikProps.handleChange}
                            value={formikProps.values.username}
                            // error={formikProps.errors.username && formikProps.touched.username}
                        />
                    </ModalBody>
                    <ModalFooter>
                        <Button onClick={handleClose} mr={3} variant='outline'>Cancel</Button>
                        <Button type="submit">
                            Submit
                        </Button>
                    </ModalFooter>
                </form>)}
        </Formik>
    )
}