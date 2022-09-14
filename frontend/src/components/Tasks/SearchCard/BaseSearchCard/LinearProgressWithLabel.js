import * as React from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import {Box, Text, Progress} from '@chakra-ui/react';


LinearProgressWithLabel.propTypes = {
    progress: PropTypes.number.isRequired,
    color: PropTypes.string.isRequired,
};

export default function LinearProgressWithLabel({progress: value, color}) {
    return (
        <Box style={{width: '100%'}}>
            <Box style={{display: 'flex', alignItems: 'center'}}>
                <Box style={{width: '100%', marginRight: "1px"}}>
                    <Progress size="lg" colorScheme={color} value={value} />
                </Box>
                <Box style={{minWidth: 35}}>
                    <Text >{`${Math.round(
                        value,
                    )}%`}</Text>
                </Box>
            </Box>
        </Box>
    );
}


