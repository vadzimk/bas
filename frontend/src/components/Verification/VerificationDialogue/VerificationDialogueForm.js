import React from 'react'
import {Formik} from "formik";

import {ModalBody, FormLabel, ModalFooter, Button, Input} from "@chakra-ui/react"

import {useDispatch, useSelector} from 'react-redux'
import {revokeTask} from "../../../reducers/searchCardsSlice";
import {loginVerificationRequested, verifyPin} from "../../../reducers/userSlice";
import {clearNotification} from "../../../reducers/notificationSlice";


export default function VerificationDialogueForm() {
    const dispatch = useDispatch()
    const user = useSelector(state => state.user)
    const task_id = user.login_verification_request?.task_id


    const card = useSelector(state =>
        state.searchCards.cards.find(c => c.tasks.find(t => t.task_id === task_id)) )


    let initialValues = {
        pin: ''
    };

    const validate = (values) => {
        const errors = {};
        if (!values.pin) {
            errors.pin = 'Required'
        }
        return errors
    }
    const handleSubmit = (fields) => {
        dispatch(verifyPin({pin:fields.pin, task_id}))
    }
    const handleRevoke = () => {
        dispatch(revokeTask({cardId: card?.id, task_id}))
        dispatch(clearNotification())
        dispatch(loginVerificationRequested(null))
    }

    return (
        <Formik
            initialValues={initialValues}
            validate={validate}
            onSubmit={handleSubmit}>
            {(formikProps) => (
                <form onSubmit={formikProps.handleSubmit}>
                    <ModalBody>
                        <FormLabel>PIN from
                            <b> {user.login_verification_request?.email}</b>
                        </FormLabel>
                        <Input
                            name="pin"
                            variant="outline"
                            onChange={formikProps.handleChange}
                            value={formikProps.values.pin}
                            // error={formikProps.errors.username && formikProps.touched.username}
                        />
                    </ModalBody>
                    <ModalFooter>
                        <Button onClick={handleRevoke} mr={3} variant='outline'>Revoke Task</Button>
                        <Button type="submit">
                            Submit
                        </Button>
                    </ModalFooter>
                </form>)}
        </Formik>
    )
}