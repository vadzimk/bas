/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React from 'react'
import {TextField} from "@mui/material";
import BasicSelect from "./BasicSelect";
import MultipleSelect from "./MultipleSelect";
import {css} from "@emotion/react";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";

const cardCss = {
    searchFlexContainer: css({
        display: 'flex',
        flexDirection: 'row',
    }),
}

const BaseSearchCardFields = ({formikProps, ...rest}) => {

    return (
        <div css={cardCss.searchFlexContainer}>
            <div>
                {/*What*/}
                <TextField
                    label="What"
                    name="what"
                    variant="outlined"
                    value={formikProps.values.what}
                    onChange={formikProps.handleChange}
                    size="small"
                    disabled={rest.formSubmitted}
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
                    size="small"
                    disabled={rest.formSubmitted}

                />
            </div>
            <div>
                {/*Radius*/}
                <BasicSelect
                    label="Radius"
                    name="radius"
                    options={rest.radiusOptions}
                    value={formikProps.values.radius}
                    onChange={(value) => formikProps.setFieldValue('radius', value)}
                    disabled={rest.formSubmitted}

                />
            </div>
            <div>
                {/*Age*/}
                <BasicSelect
                    label="Date"
                    name="age"
                    options={rest.ageOptions}
                    value={formikProps.values.age}
                    onChange={(value) => formikProps.setFieldValue('age', value)}
                    disabled={rest.formSubmitted}

                />
            </div>
            <div>
                {/*Experience*/}
                <MultipleSelect
                    label="Experience"
                    name="experience"
                    options={rest.experienceOptions}
                    value={formikProps.values.experience}
                    onChange={(value) => formikProps.setFieldValue('experience', value)}
                    disabled={rest.formSubmitted}


                />
            </div>
            <div>
                <TextField
                    label="Limit"
                    variant="outlined"
                    name="limit"
                    value={formikProps.values.limit}
                    onChange={formikProps.handleChange}
                    size="small"
                    sx={{width: 70}}
                    disabled={rest.formSubmitted}

                />
            </div>
            <div>
                <Button
                    variant="outlined"
                    sx={{height: "100%"}}
                    type="submit"
                    disabled={rest.formSubmitted}
                >
                    Submit
                </Button>
            </div>

        </div>

    )

}
export default BaseSearchCardFields