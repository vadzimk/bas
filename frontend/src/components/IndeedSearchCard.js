import React from 'react';
import BaseSearchCard from "./BaseSearchCard";
import PropTypes from "prop-types";


IndeedSearchCard.propTypes = {
    onDelete: PropTypes.func.isRequired,
    cardId: PropTypes.number.isRequired
}

export function IndeedSearchCard(props) {
    const RADIUS_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'exact', value: '&radius=0'},
        {label: '5mi', value: '&radius=5'},
        {label: '10mi', value: '&radius=10'},
        {label: '15mi', value: '&radius=10'},
        {label: '25mi', value: '&radius=25'},
        {label: '100mi', value: '&radius=100'},
    ]
    const EXPERIENCE_OPTIONS = [
        {label: 'all', value: ''},
        {label: 'entry level', value: '2'},
        {label: 'mid', value: '4'},
        {label: 'senior', value: '5'},
    ]
    const AGE_OPTIONS = [
        {label: 'all', value: ''},
        {label: '1 day', value: '&f_TPR=r86400'},
        {label: '3 day', value: '&f_TPR=r86400'},
        {label: '7 day', value: '&f_TPR=r86400'},
        {label: '14 days', value: '&f_TPR=r86400'},

    ]
    const EDUCATION_OPTIONS = [
        {label: 'school', value: 'school'},
        {label: 'associates', value: 'school'},
        {label: 'bachelors', value: 'school'},
        {label: 'masters', value: 'school'},
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