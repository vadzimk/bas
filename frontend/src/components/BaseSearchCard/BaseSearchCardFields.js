/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React from 'react'
import {TextField} from "@mui/material";
import BasicSelect from "./BasicSelect";
import MultipleSelect from "./MultipleSelect";
import {css} from "@emotion/react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";

const cardCss = {
    searchFlexContainer: css({
        display: 'flex',
        flexDirection: 'row',
    }),
}

const optionShape = PropTypes.shape({
    label: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired
})

export const searchOptionsPropTypes = {
    radiusOptions: PropTypes.arrayOf(optionShape),
    experienceOptions: PropTypes.arrayOf(optionShape),
    ageOptions: PropTypes.arrayOf(optionShape),
}

BaseSearchCardFields.propTypes = {
    formikProps: PropTypes.any,
    formSubmitted: PropTypes.bool.isRequired,
    enabledRadiusDateExperienceLimit: PropTypes.bool.isRequired,
    ...searchOptionsPropTypes
}

export default function BaseSearchCardFields({formikProps, ...rest}) {
    return (
        <div css={cardCss.searchFlexContainer}>
            <div style={{width: 225}}>
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
            <div style={{width: 225}}>
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
            <div style={{width: 95}}>
                {/*Radius*/}
                <BasicSelect
                    label="Radius"
                    name="radius"
                    options={rest.radiusOptions}
                    value={formikProps.values.radius}
                    onChange={(value) => formikProps.setFieldValue('radius', value)}
                    disabled={!rest.enabledRadiusDateExperienceLimit}

                />
            </div>
            <div style={{width: 95}}>
                {/*Age*/}
                <BasicSelect
                    label="Date"
                    name="age"
                    options={rest.ageOptions}
                    value={formikProps.values.age}
                    onChange={(value) => formikProps.setFieldValue('age', value)}
                    disabled={!rest.enabledRadiusDateExperienceLimit}

                />
            </div>
            <div style={{width: 200}}>
                {/*Experience*/}
                <rest.ExperienceSelect
                    label="Experience"
                    name="experience"
                    options={rest.experienceOptions}
                    value={formikProps.values.experience}
                    onChange={(value) => formikProps.setFieldValue('experience', value)}
                    disabled={!rest.enabledRadiusDateExperienceLimit}
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
                    disabled={!rest.enabledRadiusDateExperienceLimit}

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
