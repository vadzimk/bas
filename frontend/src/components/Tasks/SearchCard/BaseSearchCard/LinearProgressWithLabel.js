import * as React from 'react';
import PropTypes from 'prop-types';
import {Box, Text, Progress} from '@chakra-ui/react';


LinearProgressWithLabel.propTypes = {
    progress: PropTypes.number.isRequired,
    color: PropTypes.string.isRequired,
};

export default function LinearProgressWithLabel({progress: value, color}) {
    return (
        <Box style={{width: '100%', marginTop: "4px"}}>
            <Box style={{display: 'flex', justifyContent: 'space-between'}}>
                <Box style={{width: '100px', marginRight: "4px", flexShrink: 0}}>
                    <Progress height="100%" colorScheme={color} value={value} style={{margin: "auto 0"}} />
                </Box>
                <Box style={{width: "50px"}}>
                    <Text >{`${Math.round(
                        value,
                    )}%`}</Text>
                </Box>
            </Box>
        </Box>
    );
}


