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
    }

    const [formSubmitted, setFormSubmitted] = useState(false)
    const [revokeDisabled, setRevokeDisabled] = useState(false)
    const [taskId, setTaskId] = useState()

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
        console.log('task_id', task_id)
    }


    const other = {...props, formSubmitted}

    async function handleRevoke() {
        console.log("revoke")
        const statusCode = await revokeSearchTask(taskId)
        statusCode === 204 && setRevokeDisabled(true)
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
            {formSubmitted &&
            <>
                <div style={{width: "10%", display: "flex", flexDirection: "column", justifyContent: "center"}}>
                    <LinearWithValueLabel/>
                </div>
                <div>
                    <Button
                        variant="outlined"
                        sx={{height: "100%"}}
                        onClick={handleRevoke}
                        disabled={revokeDisabled}

                    >
                        Revoke
                    </Button>
                </div>

            </>
            }
            <div>
                <Button variant="outlined"
                        sx={{height: "100%"}}
                        onClick={() => props.onDelete()}
                        disabled={formSubmitted && !revokeDisabled}
                >
                    <DeleteIcon/>
                </Button>
            </div>
        </div>
    )
}

export default BaseSearchCard