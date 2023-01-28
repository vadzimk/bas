import React from 'react';

import {JobBoardContext} from "../index";
import BasicSelect from "../BaseSearchCard/BasicSelectChakra";
import BaseSearchCard from "../BaseSearchCard";
import BuiltinSearchCardFields from "./BuiltinSearchCardFields";

    export const JOB_CATEGORY_OPTIONS = [
        {value: "", label: "ALL",},
        {value: 147, label: "Data + Analytics",},
        {value: 148, label: "Design + UX",},
        {value: 149, label: "Developer + Engineer",},
        {value: 146, label: "Finance",},
        {value: 150, label: "HR",},
        {value: 151, label: "Internships",},
        {value: 152, label: "Legal",},
        {value: 153, label: "Marketing",},
        {value: 154, label: "Operations",},
        {value: 155, label: "Product",},
        {value: 156, label: "Project Mgmt",},
        {value: 157, label: "Sales",},
        {value: 158, label: "Content",}
    ]

export function BuiltinSearchCard(props) {


    const initialValues = {
        what: '',
        where: '',
        job_category: '',
        limit: '',
    }

    const validate = (values) => {
        const errors = {};
        // TODO where is not implemented and disabled
        // if (!values.where) {
        //     errors.where = 'Required'
        // }
        if (values.limit && !Number.isInteger(Number(values.limit))) {
            errors.limit = 'Integer expected'
        }
        if (!values.job_category) {
            errors.job_category = 'Required'
        }
        return errors
    }
    return (
        <JobBoardContext.Provider value={{
            initialValues: initialValues,
            jobCategoryOptions: JOB_CATEGORY_OPTIONS,
            JobCategorySelect: BasicSelect,
            validate: validate,
        }}>
            <BaseSearchCard
                CardFields={BuiltinSearchCardFields}
            />
        </JobBoardContext.Provider>
    )
}