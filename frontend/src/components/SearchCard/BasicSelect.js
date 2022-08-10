import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function BasicSelect({value, label, onChange, options}) {

    return (
        <Box sx={{minWidth: 120}}>
            <FormControl sx={{minWidth: 120}} size="small">
                <InputLabel>{label}</InputLabel>
                <Select
                    value={value}
                    onChange={e => onChange(e.target.value)}
                    // disabled={true}
                >
                    {options.map(option =>
                        <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>)}
                </Select>
            </FormControl>
        </Box>
    );
}
