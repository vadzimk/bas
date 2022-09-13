import React from 'react'
import {Formik} from "formik";
import PropTypes from "prop-types";
import {FormLabel, ModalFooter, Button, Input, FormControl, FormHelperText, FormErrorMessage} from "@chakra-ui/react"

UserDetailsForm.propTypes = {
    handleClose: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
}

export default function UserDetailsForm({handleClose, handleSubmit}) {
    const initialValues = {
        linkedin_email: '',
        linkedin_password: 'GJrPhL3ErSTJ9UE'
    }
    const validate = (values) => {
        const errors = {};
        if (!values.linkedin_email) {
            errors.linkedin_email = 'Required';
        } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.linkedin_email)) {
            errors.linkedin_email = 'Invalid email address';
        }
        if (!values.linkedin_password) {
            errors.linkedin_password = "Required"
        } else if (values.linkedin_password.length < 8) {
            errors.linkedin_password = "min length is 8"
        }
        return errors;
    }
    return (
        <Formik
            initialValues={initialValues}
            validate={validate}
            onSubmit={handleSubmit}>
            {(formikProps) => (
                <form onSubmit={formikProps.handleSubmit}>
                    <FormControl mt={4}>
                        <FormLabel>Mock Linkedin Email</FormLabel>
                        <Input
                            placeholder="Mock Linkedin Email"
                            type="email"
                            name="linkedin_email"
                            onChange={formikProps.handleChange}
                            value={formikProps.values.linkedin_email}
                        />
                        {!(formikProps.errors.linkedin_email && formikProps.touched.linkedin_email)
                        && <FormErrorMessage>
                            {formikProps.errors.linkedin_email}
                        </FormErrorMessage>
                        }
                    </FormControl>
                    <FormControl mt={4}>
                         <FormLabel size="sx">Mock Linkedin Password</FormLabel>
                        <Input
                            placeholder="Mock Linkedin Password"
                            name="linkedin_password"
                            onChange={formikProps.handleChange}
                            value={formikProps.values.linkedin_password}
                        />
                        {!(formikProps.errors.linkedin_password && formikProps.touched.linkedin_password)
                        && <FormErrorMessage>
                            {formikProps.errors.linkedin_password}
                        </FormErrorMessage>
                        }
                    </FormControl>
                    <ModalFooter>
                        <Button onClick={handleClose} mr={3}>Cancel</Button>
                        <Button type="submit">
                            Submit
                        </Button>
                    </ModalFooter>
                </form>
            )}
        </Formik>
    )
}