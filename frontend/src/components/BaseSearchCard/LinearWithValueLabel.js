import * as React from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import {updateProgress} from "../../services/searchService";

function LinearProgressWithLabel(props) {
    return (
        <Box sx={{display: 'flex', alignItems: 'center'}}>
            <Box sx={{width: '100%', mr: 1}}>
                <LinearProgress variant="determinate" {...props} />
            </Box>
            <Box sx={{minWidth: 35}}>
                <Typography variant="body2" color="text.secondary">{`${Math.round(
                    props.value,
                )}%`}</Typography>
            </Box>
        </Box>
    );
}

LinearProgressWithLabel.propTypes = {
    /**
     * The value of the progress indicator for the determinate and buffer variants.
     * Value between 0 and 100.
     */
    value: PropTypes.number.isRequired,
};

export default function LinearWithValueLabel(props) {
    const [taskId, setTaskId] = React.useState(null)
    const [progress, setProgress] = React.useState(0);
    const [progressData, setProgressData] = React.useState(null)
    const isFinished = progressData &&
        (progressData.state === 'SUCCESS' || progressData.state === 'REVOKED' || progressData.state === 'FAILURE')


    //"info": {
    //         "total": int,
    //         "current": int,
    //         "job_count": int
    //     }

    const handleUpdateProgress = async () => {
        const data = await updateProgress(taskId)
        console.log(data)
        setProgressData(data)
        if (data.state === 'PROGRESS') {
            const progressValue = 100 * data.info.current / data.info.total
            setProgress(progressValue)
            console.log("progressValue", progressValue)
        } else if (data.state === 'SUCCESS') {
            setProgress(100)
            props.onSuccess()
        } else if(data.state==='FAILURE'){
            props.onFailure(data.info)
        }
    }

    React.useEffect(() => {
        if (props.taskId !== taskId) {
            setTaskId(props.taskId)
            setProgress(0)
            setProgressData(null)
        }
    }, [props.taskId, taskId])

    React.useEffect(() => {
        const timer = !isFinished && setInterval(() => handleUpdateProgress(), 5000)
        return timer ? (() => clearInterval(timer)) : undefined
    }, [taskId, isFinished]);

    return (
        <Box sx={{width: '100%'}}>
            <LinearProgressWithLabel value={progress}/>
        </Box>
    );
}
