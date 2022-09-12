import * as React from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';


LinearProgressWithLabel.propTypes = {
    progress: PropTypes.number.isRequired,
    color: PropTypes.string.isRequired,
};

export default function LinearProgressWithLabel({progress: value, color}) {
    return (
        <Box sx={{width: '100%'}}>
            <Box sx={{display: 'flex', alignItems: 'center'}}>
                <Box sx={{width: '100%', mr: 1}}>
                    <LinearProgress variant="determinate" color={color} value={value} />
                </Box>
                <Box sx={{minWidth: 35}}>
                    <Typography variant="body2" color="text.secondary">{`${Math.round(
                        value,
                    )}%`}</Typography>
                </Box>
            </Box>
        </Box>
    );
}


