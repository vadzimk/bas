import React, {useState} from 'react';
import {Select} from 'chakra-react-select';
import PropTypes from "prop-types";

MultipleSelect.propTypes = {
    label: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    value: PropTypes.any,
    options: PropTypes.array.isRequired,
    disabled: PropTypes.bool.isRequired,
}
export default function MultipleSelect({label, onChange, value, options, disabled}) {
    const [items, setItems] = useState([]);
    const handleChange = (value) => {
        const isReset = value[value.length - 1]?.label === 'all'
        let newValue = [...value]
        if (isReset) {
            newValue = options.filter(v => v.label === 'all')
        } else {
            if (newValue[0]?.label === 'all') {
                newValue.shift()
            }
        }
        setItems(newValue);

        // pass to formik array of objects from the range of options that are selected in this component
        onChange(newValue)
    };


    return (
        <div>
            <Select
                placeholder={label}
                isMulti={true}
                value={value}
                onChange={handleChange}
                isDisabled={disabled}
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
        </div>
    );
}


