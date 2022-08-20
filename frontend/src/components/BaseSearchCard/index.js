import React, {useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields from "./BaseSearchCardFields";
import {createSearch, revokeSearchTask} from "../../services/searchService";
import LinearWithValueLabel from "./LinearWithValueLabel";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";


const BaseSearchCard = (props) => {
    const initialValues = {
        what: '',
        where: '',
        radius: '',
        age: '',
        experience: [],
        limit: '',
    }

    const [formSubmitted, setFormSubmitted] = useState(false)
    const [taskDone, setTaskDone] = useState(false)
    const [taskId, setTaskId] = useState(null)
    const [formValues, setFormValues] = useState(initialValues)
    const [message, setMessage] = useState('')
    const showProgressBar = formSubmitted
    const showRevoke = formSubmitted && !taskDone
    const showRestart = formSubmitted && taskDone
    const enabledRadiusDateExperienceLimit =false
    const enabledDeleteButton = !formSubmitted || taskDone

    const handleSubmit = async (values) => {
        console.log('values', values)
        console.log('submit')
        const {task_id} = await createSearch(
            {
                ...values,
                experience: values.experience.map(item => item.value)
            })
        setTaskId(task_id)
        setFormSubmitted(true)
        setFormValues(values)
        console.log('task_id', task_id)
    }


    const other = {...props, formSubmitted, }

    async function handleRevoke() {
        console.log("revoke")
        const statusCode = await revokeSearchTask(taskId)
        statusCode === 204 && setTaskDone(true)
    }

    const handleRestart = async () => {
        setTaskDone(false)
        setMessage('')
        await handleSubmit(formValues)
    }
    const handleFailure = (message) => {
        setTaskDone(true)
        setMessage(message)
    }

    // TODO decide what happens in case of failed task
    return (
        <div style={{display: "flex", flexDirection: "row", gap: "10px", margin: "10px 0"}}>
            <div>
                <Formik onSubmit={handleSubmit} initialValues={initialValues}>
                    {(formikProps) => {
                        return (
                            <Form>
                                <BaseSearchCardFields formikProps={formikProps} {...other}/>
                            </Form>
                        )
                    }}
                </Formik>
            </div>
            {formSubmitted &&
            <>
                <div style={{width: "10%", display: "flex", flexDirection: "column", justifyContent: "center"}}>
                    <LinearWithValueLabel
                        taskId={taskId}
                        onSuccess={() => setTaskDone(true)}
                        onFailure={(message) => handleFailure(message)}
                    />
                </div>
                <div style={{width: "95px"}}>
                    {!taskDone ?
                        <Button
                            variant="outlined"
                            sx={{height: "100%", width: "100%"}}
                            onClick={handleRevoke}
                            disabled={taskDone}
                        >
                            Revoke
                        </Button>
                        :
                        <Button
                            variant="outlined"
                            sx={{height: "100%", width: "100%"}}
                            onClick={handleRestart}
                            disabled={!taskDone}
                        >
                            Restart
                        </Button>
                    }
                </div>
            </>
            }
            <div>
                <Button variant="outlined"
                        sx={{height: "100%"}}
                        onClick={() => props.onDelete()}
                        disabled={formSubmitted && !taskDone}
                >
                    <DeleteIcon/>
                </Button>
            </div>
            { message &&
                <div>{message}</div>
            }
        </div>
    )
}

export default BaseSearchCard