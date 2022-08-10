import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import Select from '@mui/material/Select';
import Checkbox from '@mui/material/Checkbox';


export default function MultipleSelect({label, name, onChange, value, options}) {
    const [items, setItems] = React.useState([]);

    const handleChange = (event, child) => {
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
        console.log('newValue', newValue)

        // pass to formik array of objects from the range of options that are selected in this component
        onChange(newValue.map(item =>
            options.find(option =>
                option.label === item)))
    };

    return (
        <div>
            <FormControl sx={{width: 300}} size="small">
                <InputLabel>{label}</InputLabel>
                <Select
                    multiple
                    value={items}
                    onChange={handleChange}
                    input={<OutlinedInput label={label}/>}
                    renderValue={(selected) => selected.join(', ')}
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
