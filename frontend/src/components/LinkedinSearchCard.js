import React from "react";
import BaseSearchCard from "./BaseSearchCard";
import PropTypes from "prop-types";

LinkedinSearchCard.propTypes = {
    onDelete: PropTypes.func.isRequired,
    cardId: PropTypes.number.isRequired
}

export default function LinkedinSearchCard (props) {
    const RADIUS_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'exact', value: 'exact'},
        {label: '5mi', value: '5mi'},
        {label: '10mi', value: '10mi'},
        {label: '25mi', value: '25mi'},
        {label: '50mi', value: '50mi'},
    ]
    const EXPERIENCE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'internship', value: 'internship'},
        {label: 'entry level', value: 'entry level'},
        {label: 'associate', value: 'associate'},
        {label: 'mid-senior', value: 'mid-senior'},
        {label: 'director', value: 'director'},
        {label: 'executive', value: 'executive'},
    ]
    const AGE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'month', value: 'month'},
        {label: 'week', value: 'week'},
        {label: 'day', value: 'day'},
    ]


    return (
        <BaseSearchCard
            radiusOptions={RADIUS_OPTIONS}
            experienceOptions={EXPERIENCE_OPTIONS}
            ageOptions={AGE_OPTIONS}
            onDelete={props.onDelete}
            {...props}
        />
    )
}

