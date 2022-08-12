import React, {useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields from "./BaseSearchCardFields";
import {createSearch} from "../../services/searchService";


const BaseSearchCard = (props) => {
    const initialValues = {
        what: '',
        where: '',
        radius: '',
        age: '',
        experience: [],
    }

    const [formDisabled, setFormDisabled] = useState(false)

    const handleSubmit = async (values) => {
        console.log('values', values)
        console.log('submit')
        await createSearch(
            {
                ...values,
                experience: values.experience.map(item => item.value)
            })

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