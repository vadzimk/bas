/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import React, {useContext, useEffect, useRef, useState} from 'react'
import {Formik, Form} from 'formik'
import {Button, Text} from "@chakra-ui/react";
import {CloseIcon} from "@chakra-ui/icons";
import {useDispatch, useSelector} from "react-redux";
import {createTask, revokeTask, updateSearchCardFormValues} from "../../../../reducers/searchCardsSlice";
import {JobBoardContext} from "../index";
import {SearchCardContext} from "../../../../App";
import LinearProgressWithLabel from "./LinearProgressWithLabel";

const colour = {
    'PENDING': 'gray',
    'BEGUN': 'blue',
    'PROGRESS': 'blue',
    'SUCCESS': 'green',
    'REVOKED': 'yellow',
    'FAILURE': 'red',
    'VERIFICATION': 'pink',
    'VERIFYING': 'blue',
    'CLEARED': 'gray',
}

export default function BaseSearchCard({CardFields}) {
    const {onDelete, cardId} = useContext(SearchCardContext)
    let {initialValues, validate} = useContext(JobBoardContext)
    const dispatch = useDispatch()
    const card = useSelector(state =>
        state.searchCards.cards.find(c => c.id === cardId))
    const currentTask = card.tasks[card.tasks.length - 1]
    const progressData = currentTask?.status
    if (card.formValues && Object.keys(card.formValues).length > 0) {
        initialValues = card.formValues
    }
    const progress = currentTask?.progress || 0
    const formRef = useRef()  // get form values as formRef.current.values
    const [formSubmitted, setFormSubmitted] = useState(false)
    const [taskDone, setTaskDone] = useState(true)
    const message = taskDone && typeof currentTask?.status?.info === "string" && currentTask?.status?.info
    const showProgressBar = formSubmitted || (!taskDone && progressData)
    const enabledDeleteButton = !formSubmitted || taskDone
    const showRevoke = formSubmitted && !taskDone
    const showRestart = formSubmitted && taskDone
    const enabledRadiusDateExperienceLimit = !formSubmitted || taskDone
    const showSubmit = !showRevoke && !showRestart
    const [timestamp, setTimestamp] = useState("")

    // console.log("showProgressBar", card.tasks[card.tasks.length-1], showProgressBar, currentTask?.status, taskDone)

    useEffect(() => {
        const taskDone = Boolean(progressData &&
            (progressData.state === 'SUCCESS'
                || progressData.state === 'REVOKED'
                || progressData.state === 'FAILURE'
                || progressData.state === 'CLEARED'
            ))
        setTaskDone(taskDone)
        setFormSubmitted(Boolean(card.submitSuccess))
        if (taskDone && currentTask?.task_timestamp) {
            const date = new Date(currentTask.task_timestamp)
            console.log("date", date)
            const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            console.log("userTimezone", userTimezone)
            const formattedDate = date.toLocaleString("en-GB", {
                timeZone: userTimezone,
                // year: "numeric",
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            })
            console.log("formattedDate", formattedDate)
            setTimestamp(formattedDate)
        }

    }, [card, progressData])


    const handleSubmit = async (formValues) => {
        const data = {
            cardId,
            job_board: card.job_board
        }
        // get value property form each field on formValues
        for (const [k, v] of Object.entries(formValues)) {
            if (typeof v === "string") {
                data[k] = v
            } else if (Array.isArray(v)) {
                data[k] = v.map(item => item.value)
            } else {
                data[k] = v?.value
            }
        }

        dispatch(createTask(data))
        setFormSubmitted(true)
        setTimestamp('')
    }

    const handleRevoke = () => {
        const {task_id} = currentTask
        dispatch(revokeTask({cardId, task_id}))
    }

    const handleRestart = async () => {
        await handleSubmit(formRef.current.values)
    }

    const handleFormBlur = (values) => {
        dispatch(updateSearchCardFormValues({id: cardId, values}))
    }


    return (
        <div style={{display: "flex", flexDirection: "row"}}>
            <div>
                <Formik onSubmit={handleSubmit} initialValues={initialValues} innerRef={formRef} validate={validate}>
                    {(formikProps) => {
                        return (
                            <Form onBlur={() => handleFormBlur(formikProps.values)}>
                                <CardFields
                                    formikProps={formikProps}
                                    formSubmitted={formSubmitted}
                                    enabledRadiusDateExperienceLimit={enabledRadiusDateExperienceLimit}
                                    showSubmit={showSubmit}
                                />
                            </Form>
                        )
                    }}
                </Formik>
            </div>
            <div style={{display: "flex", flexDirection: "row", gap: "4px",}}>
                <div>
                    {showRevoke &&
                        <Button
                            variant="outline"
                            style={{width: "85px"}}
                            onClick={handleRevoke}
                            disabled={taskDone}
                            size='sm'
                        >
                            Revoke
                        </Button>
                    }
                    {showRestart &&
                        <Button
                            variant="outline"
                            style={{width: "85px"}}
                            onClick={handleRestart}
                            disabled={!taskDone}
                            size='sm'
                        >
                            Restart
                        </Button>
                    }
                </div>
                <div>
                    <Button variant="outline"
                            onClick={() => onDelete()}
                            disabled={!enabledDeleteButton}
                            size="sm"
                    >
                        <CloseIcon/>
                    </Button>
                </div>
                {
                    showProgressBar &&
                    <div style={{
                        width: "100px",
                        flexShrink: 0,
                        display: "flex",
                        flexDirection: "column",
                        // justifyContent: "center"
                    }}>
                        <LinearProgressWithLabel
                            progress={progress}
                            color={progressData ? colour[progressData.state] : 'secondary'}
                        />
                    </div>
                }
                {timestamp &&
                    <div style={{
                        height: "32px",
                        lineHeight: "32px",
                        textAlign: "center",
                        fontSize: "13px",
                        width: "100px"
                    }}>
                        {timestamp}
                    </div>
                }
                {message &&
                    <div style={{
                        display: "flex", maxHeight: "60px", maxWidth: "900px",
                        overflow: "hidden",
                        padding: "5px 3px",
                        fontSize: "13px",
                    }}>
                        {message}
                    </div>
                }
            </div>
        </div>
    )
}

