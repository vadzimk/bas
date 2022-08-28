import * as React from 'react';
import PropTypes from 'prop-types';
import LinearProgress from '@mui/material/LinearProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import {updateProgress} from "../../services/searchService";

LinearProgressWithLabel.propTypes = {
    value: PropTypes.number.isRequired,
    color: PropTypes.string.isRequired,
};
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


LinearWithValueLabel.propTypes={
    taskId: PropTypes.string,
    onSuccess: PropTypes.func.isRequired,
    onFailure: PropTypes.func.isRequired
}
// TODO right now polling is done inside this component but there will come time when this should be moved to one of the ancestor components
export default function LinearWithValueLabel(props) {
    const [taskId, setTaskId] = React.useState(null)
    const [progress, setProgress] = React.useState(0);
    const [progressData, setProgressData] = React.useState(null)
    const isFinished = progressData &&
        (progressData.state === 'SUCCESS' || progressData.state === 'REVOKED' || progressData.state === 'FAILURE')
    const colour = {
        'PENDING': 'secondary',
        'BEGUN': 'primary',
        'PROGRESS': 'primary',
        'SUCCESS': 'success',
        'REVOKED': 'warning',
        'FAILURE': 'error'
    }

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
            <LinearProgressWithLabel
                value={progress}
                color={progressData ? colour[progressData.state] : 'secondary'}
            />
        </Box>
    );
}
