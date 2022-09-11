/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React, {useContext} from 'react'
import {TextField} from "@mui/material";
import BasicSelect from "./BasicSelect";
import MultipleSelect from "./MultipleSelect";
import {css} from "@emotion/react";
import Button from "@mui/material/Button";
import PropTypes from "prop-types";
import {JobBoardContext} from "../SearchCard";

const cardCss = {
    searchFlexContainer: css({
        display: 'flex',
        flexDirection: 'row',
        gap: "4px",
    }),
}

BaseSearchCardFields.propTypes = {
    formikProps: PropTypes.any,
    formSubmitted: PropTypes.bool.isRequired,
    enabledRadiusDateExperienceLimit: PropTypes.bool.isRequired,
    showSubmit: PropTypes.bool.isRequired,
}

export default function BaseSearchCardFields({formikProps,formSubmitted, showSubmit,enabledRadiusDateExperienceLimit}) {
    const {
        radiusOptions,
        experienceOptions,
        ageOptions,
        ExperienceSelect
    } = useContext(JobBoardContext)

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
                    disabled={formSubmitted}
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
                    disabled={formSubmitted}

                />
            </div>
            <div style={{width: 95}}>
                {/*Radius*/}
                <BasicSelect
                    label="Radius"
                    name="radius"
                    options={radiusOptions}
                    value={formikProps.values.radius}
                    onChange={(value) => formikProps.setFieldValue('radius', value)}
                    disabled={!enabledRadiusDateExperienceLimit}

                />
            </div>
            <div style={{width: 95}}>
                {/*Age*/}
                <BasicSelect
                    label="Date"
                    name="age"
                    options={ageOptions}
                    value={formikProps.values.age}
                    onChange={(value) => formikProps.setFieldValue('age', value)}
                    disabled={!enabledRadiusDateExperienceLimit}

                />
            </div>
            <div style={{width: 200}}>
                {/*Experience*/}
                <ExperienceSelect
                    label="Experience"
                    name="experience"
                    options={experienceOptions}
                    value={formikProps.values.experience}
                    onChange={(value) => formikProps.setFieldValue('experience', value)}
                    disabled={!enabledRadiusDateExperienceLimit}
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
                    disabled={!enabledRadiusDateExperienceLimit}

                />
            </div>
            <div>
                {showSubmit &&
                    <Button
                    variant="outlined"
                    sx={{height: "100%", width: "85px"}}
                    type="submit"
                    disabled={formSubmitted}
                >
                    Submit
                </Button>}
            </div>

        </div>
    )
}
