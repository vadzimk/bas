import React, {useEffect, useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields, {searchOptionsPropTypes} from "./BaseSearchCardFields";
import {createSearch, revokeSearchTask} from "../../services/searchService";
import LinearWithValueLabel from "./LinearWithValueLabel";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import PropTypes from "prop-types";

BaseSearchCard.propTypes = {
    onDelete: PropTypes.func.isRequired,
    userId: PropTypes.number.isRequired,
    handleAccountFailure: PropTypes.func.isRequired,
    ...searchOptionsPropTypes
}
export default function BaseSearchCard({onDelete, userId, handleAccountFailure, ...rest}) {
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
    const enabledRadiusDateExperienceLimit = !formSubmitted || taskDone
    const enabledDeleteButton = !formSubmitted || taskDone
    const other = {...rest, formSubmitted, enabledRadiusDateExperienceLimit}

    const handleSubmit = async (values) => {
        console.log('values', values)
        console.log('submit')
        const {task_id} = await createSearch(
            {
                ...values,
                experience: values.experience.map(item => item.value),
                user_id: userId
            })
        setTaskId(task_id)
        setFormSubmitted(true)
        setFormValues(values)
        console.log('task_id', task_id)
    }


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
        if (message.includes('Linkedin account')) {
            handleAccountFailure()
            console.log('handleFailure')
        }
    }

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
            <>
                {showProgressBar &&
                <div style={{width: "10%", display: "flex", flexDirection: "column", justifyContent: "center"}}>
                    <LinearWithValueLabel
                        taskId={taskId}
                        onSuccess={() => setTaskDone(true)}
                        onFailure={(message) => handleFailure(message)}
                    />
                </div>
                }
                <div>
                    {showRevoke &&
                    <Button
                        variant="outlined"
                        sx={{height: "100%", width: "95px"}}
                        onClick={handleRevoke}
                        disabled={taskDone}
                    >
                        Revoke
                    </Button>
                    }
                    {showRestart &&
                    <Button
                        variant="outlined"
                        sx={{height: "100%", width: "95px"}}
                        onClick={handleRestart}
                        disabled={!taskDone}
                    >
                        Restart
                    </Button>
                    }
                </div>
            </>
            <div>
                <Button variant="outlined"
                        sx={{height: "100%"}}
                        onClick={() => onDelete()}
                        disabled={!enabledDeleteButton}
                >
                    <DeleteIcon/>
                </Button>
            </div>
            {message &&
            <div style={{display: "flex", alignItems: "center"}}><p>{message}</p></div>
            }
        </div>
    )
}

