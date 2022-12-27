/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */
// the above comments are necessary to make the css prop work

import React, {useContext} from 'react'
import PropTypes from "prop-types";
import {JobBoardContext} from "../index";
import {Input, Button} from "@chakra-ui/react";
import BasicSelect from "../BaseSearchCard/BasicSelectChakra";


BaseCardFields.propTypes = {
    formikProps: PropTypes.any,
    formSubmitted: PropTypes.bool.isRequired,
    enabledRadiusDateExperienceLimit: PropTypes.bool.isRequired,
    showSubmit: PropTypes.bool.isRequired,
}

export default function BaseCardFields({
                                           formikProps,
                                           formSubmitted,
                                           showSubmit,
                                           enabledRadiusDateExperienceLimit
                                       }) {
    const {
        jobCategoryOptions,
        JobCategorySelect
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
                    // disabled={formSubmitted}
                    disabled={true} // TODO field not implemented
                    borderRadius="base"
                    isInvalid={formikProps.errors.where && formikProps.touched.where}
                    errorBorderColor='red.200'
                />
            </div>

            <div style={{width: 596}}>
                {/*job_category*/}
                <JobCategorySelect
                    label="Job Category"
                    name="job_category"
                    options={jobCategoryOptions}
                    value={formikProps.values.job_category}
                    onChange={(value) => formikProps.setFieldValue('job_category', value)}
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
