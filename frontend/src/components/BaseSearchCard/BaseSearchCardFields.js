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
                    disabled={rest.formDisabled}
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
                    disabled={rest.formDisabled}

                />
            </div>
            <div>
                {/*Distance*/}
                <BasicSelect
                    label="Distance"
                    name="distance"
                    options={rest.distanceOptions}
                    value={formikProps.values.distance}
                    onChange={(value) => formikProps.setFieldValue('distance', value)}
                    disabled={rest.formDisabled}

                />
            </div>
            <div>
                {/*Date*/}
                <BasicSelect
                    label="Date"
                    name="date"
                    options={rest.dateOptions}
                    value={formikProps.values.date}
                    onChange={(value) => formikProps.setFieldValue('date', value)}
                    disabled={rest.formDisabled}

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
                    disabled={rest.formDisabled}


                />
            </div>
            <div>
                <Button variant="outlined"
                        sx={{height: "100%"}}
                        onClick={() => rest.onDelete()}
                        disabled={rest.formDisabled}

                >
                    <DeleteIcon/>
                </Button>
            </div>
            <div>
                <Button
                    variant="outlined"
                    sx={{height: "100%"}}
                    type="submit"
                    disabled={rest.formDisabled}

                >
                    Submit
                </Button>
            </div>

        </div>

    )

}
export default BaseSearchCardFields