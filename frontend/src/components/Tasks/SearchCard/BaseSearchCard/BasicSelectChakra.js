import React from 'react';
import PropTypes from "prop-types";
import {Select} from 'chakra-react-select'

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
            options={options}
            onChange={onChange}
            isDisabled={disabled}
            style={{width: "100%"}}
            size="sm"
            useBasicStyles
            isClearable={true}
            chakraStyles={{
                control: provided => ({
                    ...provided,
                    borderRadius: "base"
                }),
            }}
        >
        </Select>

    );
}
