import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';
import PropTypes from "prop-types";

MultipleSelect.propTypes={
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    value: PropTypes.any,
    options: PropTypes.array.isRequired,
    disabled: PropTypes.bool.isRequired,
}
export default function MultipleSelect({label, onChange, value, options, disabled}) {
    const [items, setItems] = React.useState([]);

    const handleChange = (event) => {
        const {value} = event.target;
        const isReset = value[value.length - 1] === 'all'
        let newValue = [...value]
        if (isReset) {
            newValue = ['all']
        } else {
            if (newValue[0] === 'all') {
                newValue.shift()
            }
        }
        setItems(newValue);

        // pass to formik array of objects from the range of options that are selected in this component
        onChange(newValue.map(item =>
            options.find(option =>
                option.label === item)))
    };

    return (
        <div>
            <FormControl sx={{width: "100%"}} size="small">
                <InputLabel>{label}</InputLabel>
                <Select
                    multiple
                    value={value.map(v=>v.label)}
                    onChange={handleChange}
                    input={<OutlinedInput label={label}/>}
                    renderValue={(selected) => selected.join(', ')}
                    disabled={disabled}
                >
                    {options.map((option) => (
                        <MenuItem key={option.label} value={option.label}>
                            <Checkbox checked={items.indexOf(option.label) > -1}/>
                            <ListItemText primary={option.label}/>
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </div>
    );
}
