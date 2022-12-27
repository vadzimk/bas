import React from 'react';

import {JobBoardContext} from "../index";
import BaseCard from "./BaseCard";
import MultipleSelect from "../BaseSearchCard/MultipleSelectChakra";


export function BuiltinSearchCard(props) {
    const JOB_CATEGORY_OPTIONS = [
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

    const initialValues = {
        what: '',
        where: '',
        jobCategory: '',
        limit: '',
    }

    return (
        <JobBoardContext.Provider value={{
            initialValues: initialValues,
            jobCategoryOptions: JOB_CATEGORY_OPTIONS,
            JobCategorySelect: MultipleSelect
        }}>
            <BaseCard/>
        </JobBoardContext.Provider>
    )
}