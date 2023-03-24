import * as React from 'react';
import PropTypes from 'prop-types';
import {Box, Text, Progress} from '@chakra-ui/react';


LinearProgressWithLabel.propTypes = {
    progress: PropTypes.number.isRequired,
    color: PropTypes.string.isRequired,
};

export default function LinearProgressWithLabel({progress: value, color}) {
    return (
        <Box style={{width: '100%', marginTop: "4px", height: "100%"}}>
            <Box style={{position: "relative", height: "100%"}}>
                <Box style={{width: '100px', marginRight: "4px", height: "24px", position: "absolute", opacity: "50%"}}>
                    <Progress height="100%" colorScheme={color} value={value} style={{margin: "auto 0"}} />
                </Box>
                <Box style={{width: "50px", position: "absolute", top: 3, left: 4, fontSize: "12px", fontWeight: "600"}}>
                    <Text style={{color: "#003eaa"}} >{`${Math.round(
                        value,
                    )}%`}</Text>
                </Box>
            </Box>
        </Box>
    );
}


