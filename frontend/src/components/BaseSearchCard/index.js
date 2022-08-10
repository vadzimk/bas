

import React from 'react'
import Button from '@mui/material/Button';
import MultipleSelect from "./MultipleSelect";
import BasicSelect from "./BasicSelect";
import {IconButton, TextField} from "@mui/material";
import {css} from "@emotion/react";
import {Formik, Form} from 'formik'
import DeleteIcon from '@mui/icons-material/Delete';
import BaseSearchCardFields from "./BaseSearchCardFields";



const BaseSearchCard = (props) => {
    const other = {...props}
    console.log('basesearchcard-other', other)
    const initialValues = {
        what: '',
        where: '',
        distance: '',
        date: '',
        experience: [],
    }

    const handleSubmit = (values) => {
        console.log('values', values)
        console.log('submit')
    }


    return (
        <Formik onSubmit={handleSubmit} initialValues={initialValues}>
            {(formikProps) => {
                console.log('formik-other', other)
                return (
                    <Form>
                        <BaseSearchCardFields formikProps={formikProps} {...other}/>
                    </Form>
                )
            }}
        </Formik>
    )
}

export default BaseSearchCard