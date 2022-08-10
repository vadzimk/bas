

import React, {useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields from "./BaseSearchCardFields";



const BaseSearchCard = (props) => {
    const initialValues = {
        what: '',
        where: '',
        distance: '',
        date: '',
        experience: [],
    }

    const [formDisabled, setFormDisabled] = useState(false)

    const handleSubmit = (values) => {
        console.log('values', values)
        console.log('submit')
        setFormDisabled(true)
    }


    const other = {...props, formDisabled}
    return (
        <Formik onSubmit={handleSubmit} initialValues={initialValues}>
            {(formikProps) => {
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