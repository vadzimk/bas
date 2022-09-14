import * as React from 'react';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import {Select} from 'chakra-react-select';
import Checkbox from '@mui/material/Checkbox';
import PropTypes from "prop-types";

MultipleSelect.propTypes = {
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    value: PropTypes.any,
    options: PropTypes.array.isRequired,
    disabled: PropTypes.bool.isRequired,
}
export default function MultipleSelect({label, onChange, value, options, disabled}) {
    const [items, setItems] = React.useState([]);

    console.log("options", options)
    console.log("incoming value", value)

    const handleChange = (value) => {
        const isReset = value[value.length - 1]?.label === 'all'
        console.log("value", value)
        console.log("is reset", isReset)
        let newValue = [...value]
        if (isReset) {
            newValue = options.filter(v => v.label === 'all')
        } else {
            if (newValue[0]?.label === 'all') {
                newValue.shift()
            }
        }
        setItems(newValue);
        console.log("out-----value", newValue)

        // pass to formik array of objects from the range of options that are selected in this component
        onChange(newValue)
    };


    return (
        <div>
            {/*<FormControl sx={{width: "100%"}} size="small">*/}
            {/*    <InputLabel>{label}</InputLabel>*/}
            <Select
                placeholder={label}
                isMulti={true}
                value={value}
                onChange={handleChange}
                // input={<OutlinedInput label={label}/>}
                // renderValue={(selected) => selected.join(', ')}
                disabled={disabled}
                options={options}
                size="sm"
                closeMenuOnSelect={false}
                useBasicStyles
                selectedOptionStyle="check"
                hideSelectedOptions={false}
                chakraStyles={{
                    control: provided => ({
                        ...provided,
                        borderRadius: "base"
                    }),

                }}

            />
            {/*    {options.map((option) => (*/}
            {/*        <MenuItem key={option.label} value={option.label}>*/}
            {/*            <Checkbox checked={items.indexOf(option.label) > -1}/>*/}
            {/*            <ListItemText primary={option.label}/>*/}
            {/*        </MenuItem>*/}
            {/*    ))}*/}
            {/*</Select>*/}
            {/*</FormControl>*/}
        </div>
    );
}


