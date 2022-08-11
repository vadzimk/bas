import React from "react";
import BaseSearchCard from "./BaseSearchCard";

const LinkedinSearchCard = (props) => {


    const RADIUS_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'exact', value: 'distance=0'},
        {label: '5mi', value: 'distance=5'},
        {label: '10mi', value: 'distance=10'},
        {label: '25mi', value: 'distance=25'},
        {label: '50mi', value: 'distance=50'},
    ]
    const EXPERIENCE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'internship', value: '1'},
        {label: 'entry level', value: '2'},
        {label: 'associate', value: '3'},
        {label: 'mid-senior', value: '4'},
        {label: 'director', value: '5'},
        {label: 'executive', value: '6'},
    ]
    const AGE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'month', value: '&f_TPR=r2592000'},
        {label: 'week', value: '&f_TPR=r604800'},
        {label: 'day', value: '&f_TPR=r86400'},
    ]


    return (
        <BaseSearchCard
            radiusOptions={RADIUS_OPTIONS}
            experienceOptions={EXPERIENCE_OPTIONS}
            ageOptions={AGE_OPTIONS}
            onDelete={props.onDelete}
        />
    )
}

export default LinkedinSearchCard