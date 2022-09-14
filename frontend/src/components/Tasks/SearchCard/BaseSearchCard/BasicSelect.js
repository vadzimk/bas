import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
// import Select from '@mui/material/Select';
import PropTypes from "prop-types";
import {Select} from '@chakra-ui/react'

BasicSelect.propTypes = {
    value: PropTypes.any,
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    options: PropTypes.array.isRequired,
    disabled: PropTypes.bool.isRequired,
}
export default function BasicSelect({value, label, onChange, options, disabled}) {

    return (
        <Select
            placeholder={label}
            value={value}
            onChange={e => onChange(e.target.value)}
            disabled={disabled}
            style={{width: "100%"}}
            borderRadius="base"
        >
            {options.map(option =>
                <option
                    key={option.value}
                    value={option.value}
                >
                    {option.label}
                </option>)}
        </Select>

    );
}
