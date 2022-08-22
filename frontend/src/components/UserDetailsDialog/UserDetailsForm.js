import React from 'react'
import {Formik} from "formik";
import TextField from "@mui/material/TextField";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

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
                    <TextField
                        margin="dense"
                        label="Fake Linkedin Email"
                        type="email"
                        name="linkedin_email"
                        fullWidth
                        variant="standard"
                        onChange={formikProps.handleChange}
                        value={formikProps.values.linkedin_email}
                        error={formikProps.errors.linkedin_email && formikProps.touched.linkedin_email}
                        helperText={formikProps.errors.linkedin_email}
                    />
                    <TextField
                        margin="dense"
                        label="Fake Linkedin Password"
                        name="linkedin_password"
                        fullWidth
                        variant="standard"
                        onChange={formikProps.handleChange}
                        value={formikProps.values.linkedin_password}
                        error={formikProps.errors.linkedin_password && formikProps.touched.linkedin_password}
                        helperText={formikProps.errors.linkedin_password}
                    />
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button type="submit">
                            Submit
                        </Button>
                    </DialogActions>
                </form>
            )}
        </Formik>
    )
}