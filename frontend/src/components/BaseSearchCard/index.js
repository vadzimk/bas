import React, {useContext, useEffect, useRef, useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields from "./BaseSearchCardFields";
import {revokeSearchTask} from "../../services/searchService";
import LinearWithValueLabel from "./LinearWithValueLabel";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import {useDispatch, useSelector} from "react-redux";
import {notify, Ntypes} from "../../reducers/notificationSlice";
import {createTask, updateSearchCard} from "../../reducers/searchCardsSlice";
import {JobBoardContext} from "../SearchCard";
import {SearchCardContext} from "../../App";


export default function BaseSearchCard() {
    const {onDelete, cardId,} = useContext(SearchCardContext)

    const [formSubmitted, setFormSubmitted] = useState(false)
    const [taskDone, setTaskDone] = useState(false)
    const [taskId, setTaskId] = useState(null)
    const [message, setMessage] = useState('')

    const showProgressBar = formSubmitted
    const showRevoke = formSubmitted && !taskDone
    const showRestart = formSubmitted && taskDone
    const enabledRadiusDateExperienceLimit = !formSubmitted || taskDone
    const enabledDeleteButton = !formSubmitted || taskDone
    const dispatch = useDispatch()
    const card = useSelector(state =>
        state.searchCards.cards.find(c => c.id === cardId))
    let {initialValues} = useContext(JobBoardContext)
    if (card.formValues && Object.keys(card.formValues).length > 0) { // has values in redux state use them
        initialValues = card.formValues
    }
    const formRef = useRef()  // get form values as formRef.current.values

    useEffect(() => {
        const tasksLength = card.tasks.length
        if (tasksLength > 0) {
            const {task_id} = card.tasks[tasksLength - 1]
            setTaskId(task_id)
        }
        console.log('task_id', card.task_id)
        console.log('card', card)

    }, [card])

    const handleSubmit = async (values) => {
        console.log('values', values)
        console.log('submit')
        console.log(typeof values.experience)
        dispatch(createTask({
            ...values,
            experience: typeof values.experience === 'string'
                ? values.experience
                : values.experience.map(item => item.value),
            cardId,
            job_board: card.job_board
        }))
        setFormSubmitted(true)
    }


    async function handleRevoke() {
        console.log("revoke")
        const statusCode = await revokeSearchTask(taskId)
        statusCode === 204 && setTaskDone(true)
    }

    const handleRestart = async () => {
        setTaskDone(false)
        setMessage('')
        await handleSubmit(formRef.current.values)
    }
    const handleFailure = (message) => {
        setTaskDone(true)
        setMessage(message)
        if (message.includes('Linkedin account')) {
            dispatch(notify({type: Ntypes.ERROR, message}))
        }
    }

    const handleFormBlur = (values) => {
        console.log('values', values)
        dispatch(updateSearchCard({id: cardId, values}))

    }


    return (
        <div style={{display: "flex", flexDirection: "row", gap: "10px"}}>
            <div>
                <Formik onSubmit={handleSubmit} initialValues={initialValues} innerRef={formRef}>
                    {(formikProps) => {
                        return (
                            <Form onBlur={() => handleFormBlur(formikProps.values)}>
                                <BaseSearchCardFields
                                    formikProps={formikProps}
                                    formSubmitted={formSubmitted}
                                    enabledRadiusDateExperienceLimit={enabledRadiusDateExperienceLimit}
                                />
                            </Form>
                        )
                    }}
                </Formik>
            </div>
            <>
                {showProgressBar &&
                <div style={{
                    width: "100px",
                    flexShrink: 0,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center"
                }}>
                    <LinearWithValueLabel
                        taskId={taskId}
                        cardId={cardId}
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

