/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React, {useContext} from 'react'
import BasicSelect from "./BasicSelectChakra";
import PropTypes from "prop-types";
import {JobBoardContext} from "../index";
import {Input, Button} from "@chakra-ui/react";


BaseSearchCardFields.propTypes = {
    formikProps: PropTypes.any,
    formSubmitted: PropTypes.bool.isRequired,
    enabledRadiusDateExperienceLimit: PropTypes.bool.isRequired,
    showSubmit: PropTypes.bool.isRequired,
}

export default function BaseSearchCardFields({
                                                 formikProps,
                                                 formSubmitted,
                                                 showSubmit,
                                                 enabledRadiusDateExperienceLimit
                                             }) {
    const {
        radiusOptions,
        experienceOptions,
        ageOptions,
        ExperienceSelect
    } = useContext(JobBoardContext)

    return (
        <div style={{display: 'flex', flexDirection: 'row', gap: "4px"}}>
            <div style={{width: 180}}>
                {/*What*/}
                <Input
                    placeholder="What"
                    name="what"
                    value={formikProps.values.what}
                    onChange={formikProps.handleChange}
                    disabled={formSubmitted}
                    borderRadius="base"
                    isInvalid={formikProps.errors.what && formikProps.touched.what}
                    errorBorderColor='red.200'
                />
            </div>
            <div style={{width: 180}}>
                {/*Where*/}
                <Input
                    placeholder="Where"
                    name="where"
                    value={formikProps.values.where}
                    onChange={formikProps.handleChange}
                    disabled={formSubmitted}
                    borderRadius="base"
                    isInvalid={formikProps.errors.where && formikProps.touched.where}
                    errorBorderColor='red.200'
                />
            </div>
            <div style={{width: 124}}>
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
            <div style={{width: 124}}>
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
            <div style={{width: 340}}>
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
                <Input
                    placeholder="Limit"
                    variant="outline"
                    name="limit"
                    value={formikProps.values.limit}
                    onChange={formikProps.handleChange}
                    style={{width: "57px"}}
                    disabled={!enabledRadiusDateExperienceLimit}
                    borderRadius="base"
                    isInvalid={formikProps.errors.limit && formikProps.touched.limit}
                    errorBorderColor='red.200'
                />
            </div>
            <div>
                {showSubmit &&
                <Button
                    // variant="outline"
                    style={{width: "85px"}}
                    type="submit"
                    disabled={formSubmitted}
                >
                    Start
                </Button>}
            </div>

        </div>
    )
}
