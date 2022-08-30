import React, {useEffect, useRef, useState} from 'react'
import {Formik, Form} from 'formik'
import BaseSearchCardFields, {searchOptionsPropTypes} from "./BaseSearchCardFields";
import {revokeSearchTask} from "../../services/searchService";
import LinearWithValueLabel from "./LinearWithValueLabel";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import PropTypes from "prop-types";
import {useDispatch, useSelector} from "react-redux";
import {notify, Ntypes} from "../../reducers/notificationSlice";
import {createTask} from "../../reducers/searchCardsSlice";

BaseSearchCard.propTypes = {
    onDelete: PropTypes.func.isRequired,
    cardId: PropTypes.number.isRequired,
    ...searchOptionsPropTypes
}
export default function BaseSearchCard({onDelete, cardId, ...rest}) {
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
    const [message, setMessage] = useState('')

    const showProgressBar = formSubmitted
    const showRevoke = formSubmitted && !taskDone
    const showRestart = formSubmitted && taskDone
    const enabledRadiusDateExperienceLimit = !formSubmitted || taskDone
    const enabledDeleteButton = !formSubmitted || taskDone
    const other = {...rest, formSubmitted, enabledRadiusDateExperienceLimit}
    const dispatch = useDispatch()
    // const userId = useSelector(state => state.user.id)
    const card = useSelector(state =>
        state.searchCards.cards.find(c => c.id === cardId))
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
        dispatch(createTask({
            ...values,
            experience: values.experience.map(item => item.value),
            cardId
        }))
        // TODO replace with dispatch
        // const {task_id} = await createSearch(
        //     {
        //         ...values,
        //         experience: values.experience.map(item => item.value),
        //         user_id: userId
        //     })
        // setTaskId(task_id)
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


    return (
        <div style={{display: "flex", flexDirection: "row", gap: "10px", margin: "10px 0"}}>
            <div>
                <Formik onSubmit={handleSubmit} initialValues={initialValues} innerRef={formRef}>
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

