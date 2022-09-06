import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import PropTypes from "prop-types";

BasicSelect.propTypes ={
    value: PropTypes.any,
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    options: PropTypes.array.isRequired,
    disabled: PropTypes.bool.isRequired,
}
export default function BasicSelect({value, label, onChange, options, disabled}) {

    return (
        <Box>
            <FormControl sx={{width: '100%'}} size="small">
                <InputLabel>{label}</InputLabel>
                <Select
                    value={value}
                    onChange={e => onChange(e.target.value)}
                    disabled={disabled}
                >
                    {options.map(option =>
                        <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>)}
                </Select>
            </FormControl>
        </Box>
    );
}
