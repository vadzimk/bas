import React from 'react'
import TextField from "@mui/material/TextField";
import {Formik} from "formik";
import PropTypes from "prop-types";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";

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
                    <TextField
                        margin="dense"
                        label="Username"
                        name="username"
                        fullWidth
                        variant="standard"
                        onChange={formikProps.handleChange}
                        value={formikProps.values.username}
                        error={formikProps.errors.username && formikProps.touched.username}
                    />
                    <DialogActions>
                        <Button onClick={handleClose}>Cancel</Button>
                        <Button type="submit">
                            Submit
                        </Button>
                    </DialogActions>
                </form>)}
        </Formik>
    )
}