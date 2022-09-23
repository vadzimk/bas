import React from 'react';
import BaseSearchCard from "./BaseSearchCard";
import BasicSelect from "./BaseSearchCard/BasicSelectChakra";
import {JobBoardContext} from "./index";


export function IndeedSearchCard(props) {
    const RADIUS_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'exact', value: 'exact'},
        {label: '5mi', value: '5mi'},
        {label: '10mi', value: '10mi'},
        {label: '15mi', value: '15mi'},
        {label: '25mi', value: '25mi'},
        {label: '100mi', value: '100mi'},
    ]
    const EXPERIENCE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'entry level', value: 'entry level'},
        {label: 'mid', value: 'mid'},
        {label: 'senior', value: 'senior'},
    ]
    const AGE_OPTIONS = [
        {label: 'all', value: ''},
        {label: '1 day', value: '1 day'},
        {label: '3 days', value: '3 days'},
        {label: '7 days', value: '7 days'},
        {label: '14 days', value: '14 days'},

    ]
    // decided to have uniform form fields
    // const EDUCATION_OPTIONS = [
    //     {label: 'school', value: 'school'},
    //     {label: 'associates', value: 'associates'},
    //     {label: 'bachelors', value: 'bachelors'},
    //     {label: 'masters', value: 'masters'},
    // ]
    const initialValues = {
        what: '',
        where: '',
        radius: '',
        age: '',
        experience: '',
        limit: '',
    }

    return (
        <JobBoardContext.Provider value={{
            initialValues: initialValues,
            radiusOptions: RADIUS_OPTIONS,
            experienceOptions: EXPERIENCE_OPTIONS,
            ageOptions: AGE_OPTIONS,
            ExperienceSelect: BasicSelect
        }}>
            <BaseSearchCard/>
        </JobBoardContext.Provider>
    )
}