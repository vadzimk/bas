/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React from 'react'
import Button from '@mui/material/Button';
import MultipleSelect from "./MultipleSelect";
import BasicSelect from "./BasicSelect";
import {TextField} from "@mui/material";
import {css} from "@emotion/react";
import {Formik, Form} from 'formik'

const cardCss = {
    searchFlexContainer: css({
        display: 'flex',
        flexDirection: 'row',
    }),
}

const BaseSearchCard = (props) => {
    const other = {...props}
    const initialValues = {
        what: '',
        where: '',
        distance: '',
        date: '',
        experience: [],
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log('submitted')
    }
    return (
        <Formik onSubmit={handleSubmit} initialValues={initialValues}>
            {(formikProps, other) => (
                <Form css={cardCss.searchFlexContainer} {...other}>
                    <div>
                        {/*What*/}
                        <TextField
                            label="What"
                            name="what"
                            variant="outlined"
                            value={formikProps.values.what}
                            onChange={formikProps.handleChange}
                        />
                    </div>
                    <div>
                        {/*Where*/}
                        <TextField
                            label="Where"
                            variant="outlined"
                            name="where"
                            value={formikProps.values.where}
                            onChange={formikProps.handleChange}
                        />
                    </div>
                    <div>
                        {/*Distance*/}
                        <BasicSelect
                            label="Distance"
                            name="distance"
                            options={props.distanceOptions}
                            value={formikProps.values.distance}
                            onChange={(value) => formikProps.setFieldValue('distance', value)}
                        />
                    </div>
                    <div>
                        {/*Date*/}
                        <BasicSelect
                            label="Date"
                            name="date"
                            options={props.dateOptions}
                            value={formikProps.values.date}
                            onChange={(value) => formikProps.setFieldValue('date', value)}
                        />
                    </div>
                    <div>
                        {/*Experience*/}
                        <MultipleSelect
                            label="Experience"
                            name="experience"
                            options={props.experienceOptions}
                            value={formikProps.values.experience}
                            onChange={(value) => formikProps.setFieldValue('experience', value)}

                        />
                    </div>
                    <div>
                        <Button variant="outlined">Create</Button>
                    </div>
                </Form>
            )}
        </Formik>
    )
}

export default BaseSearchCard