/* eslint-disable react/react-in-jsx-scope -- Unaware of jsxImportSource */
/** @jsxImportSource @emotion/react */

import React, {useContext, useRef} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields from "./BaseSearchCardFields";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import {useDispatch, useSelector} from "react-redux";
import {createTask, revokeTask, updateSearchCardFormValues} from "../../reducers/searchCardsSlice";
import {JobBoardContext} from "../SearchCard";
import {SearchCardContext} from "../../App";
import LinearProgressWithLabel from "./LinearProgressWithLabel";
import theme from "../../Theme";

const colour = {
    'PENDING': 'secondary',
    'BEGUN': 'primary',
    'PROGRESS': 'primary',
    'SUCCESS': 'success',
    'REVOKED': 'warning',
    'FAILURE': 'error'
}

export default function BaseSearchCard() {
    const {onDelete, cardId,} = useContext(SearchCardContext)
    const dispatch = useDispatch()
    const card = useSelector(state =>
        state.searchCards.cards.find(c => c.id === cardId))
    const currentTask = card.tasks[card.tasks.length - 1]
    const progressData = currentTask?.status
    console.log("currentTask", currentTask)
    const taskDone = Boolean(progressData &&
        (progressData.state === 'SUCCESS' || progressData.state === 'REVOKED' || progressData.state === 'FAILURE'))
    const message = taskDone && typeof currentTask.status.info === "string" && currentTask.status.info
    const formSubmitted = Boolean(card.submitSuccess)
    const showProgressBar = formSubmitted || currentTask
    const showRevoke = formSubmitted && !taskDone
    const showRestart = formSubmitted && taskDone
    const showSubmit = !showRevoke && !showRestart
    const enabledRadiusDateExperienceLimit = !formSubmitted || taskDone
    const enabledDeleteButton = !formSubmitted || taskDone
    let {initialValues} = useContext(JobBoardContext)
    if (card.formValues && Object.keys(card.formValues).length > 0) {
        initialValues = card.formValues
    }
    const progress = currentTask?.progress || 0
    const formRef = useRef()  // get form values as formRef.current.values

    const handleSubmit = async (values) => {
        console.log('values', values)
        console.log('submit')
        dispatch(createTask({
            ...values,
            experience: typeof values.experience === 'string'
                ? values.experience
                : values.experience.map(item => item.value),
            cardId,
            job_board: card.job_board
        }))
    }

    const handleRevoke = () => {
        const {task_id} = currentTask
        dispatch(revokeTask({cardId, task_id}))
    }

    const handleRestart = async () => {
        await handleSubmit(formRef.current.values)
    }

    const handleFormBlur = (values) => {
        console.log('values', values)
        dispatch(updateSearchCardFormValues({id: cardId, values}))
    }


    return (
        <div style={{display: "flex", flexDirection: "row", alignItems: "center"}}>
            <div>
                <Formik onSubmit={handleSubmit} initialValues={initialValues} innerRef={formRef}>
                    {(formikProps) => {
                        return (
                            <Form onBlur={() => handleFormBlur(formikProps.values)}>
                                <BaseSearchCardFields
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
            <div style={{display: "flex", flexDirection: "row", gap: "4px", alignItems: "center"}}>
                <div style={{maxHeight: "40px"}}>
                    {showRevoke &&
                    <Button
                        variant="outlined"
                        sx={{height: "100%", width: "85px"}}
                        onClick={handleRevoke}
                        disabled={taskDone}
                    >
                        Revoke
                    </Button>
                    }
                    {showRestart &&
                    <Button
                        variant="outlined"
                        sx={{height: "100%", width: "85px"}}
                        onClick={handleRestart}
                        disabled={!taskDone}
                    >
                        Restart
                    </Button>
                    }
                </div>
                <div style={{maxHeight: "40px"}}>
                    <Button variant="outlined"
                            sx={{height: "100%"}}
                            onClick={() => onDelete()}
                            disabled={!enabledDeleteButton}
                    >
                        <DeleteIcon/>
                    </Button>
                </div>
                {
                    showProgressBar &&
                    <div style={{
                        width: "100px",
                        flexShrink: 0,
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "center"
                    }}>
                        <LinearProgressWithLabel
                            progress={progress}
                            color={progressData ? colour[progressData.state] : 'secondary'}
                        />
                    </div>
                }
                {message &&
                <div style={{display: "flex", alignItems: "center", maxHeight: "60px"}}><p
                    css={theme.typography.p}>{message}</p></div>
                }
            </div>
        </div>
    )
}

