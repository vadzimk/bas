import {createAsyncThunk, createSlice} from "@reduxjs/toolkit"
import api from "../services/api";
import {revokeSearchTask, updateProgress} from "../services/searchService";
import {clearNotification, notify, notifyTemp, Ntypes} from "./notificationSlice";
import {fetchResults} from "./resultsSlice";
import {func} from "prop-types";
import {loginVerificationRequested} from "./userSlice";
import {JOB_CATEGORY_OPTIONS} from '../components/Tasks/SearchCard/BuiltinSearchCard'

const initialState = {
    cards: [],
    nextCardId: 0,

}

// task interface {task_id, timer, status:{state, info}}

const searchCardsSlice = createSlice({
    name: "tasks",
    initialState,
    reducers: {
        addSearchCard: function (state, action) {
            const newCard = {
                id: state.nextCardId,
                tasks: [],
                model_id: null,
                formValues: {},
                job_board: action.payload,
                submitSuccess: null,
                isChecked: true,
            }
            state.cards = [...state.cards, newCard]
            state.nextCardId = state.nextCardId + 1
        },
        deleteUnSubmittedCard: function (state, action) {
            state.cards = state.cards.filter(c => c.id !== action.payload)
        },
        updateSearchCardFormValues: function (state, action) {
            state.cards = state.cards.map(c => {
                if (c.id === action.payload.id) {
                    return {...c, formValues: action.payload.values}
                } else {
                    return {...c}
                }
            })
        },
        updateSearchCardTaskStatus: function (state, action) {
            const {model_id, task_id, data} = action.payload
            const computeProgress = (data) => {
                if (data.state === 'PROGRESS') {
                    return 100 * data.info.current / data.info.total
                } else if (data.state === 'SUCCESS') {
                    return 100
                } else return undefined
            }
            const progress = computeProgress(data)
            state.cards = state.cards.map(c => {
                if (c.model_id === model_id) {
                    return {
                        ...c,
                        tasks: c.tasks.map(t => t.task_id === task_id ? {
                            ...t,
                            status: data,
                            progress: progress || t.progress
                        } : {...t})
                    }
                } else {
                    return c
                }
            })
        },
        toggledCard: function (state, action) {
            const cardId = action.payload
            state.cards = state.cards.map(c =>
                c.id === cardId ? {...c, isChecked: !c.isChecked} : {...c}
            )
        },
        setAllCardsChecked: function (state, action) {
            state.cards = state.cards.map(c => ({...c, isChecked: action.payload})
            )
        }
    },
    extraReducers: builder => {
        builder.addCase(createTask.fulfilled, (state, action) => {
            const {task_id, model_id, cardId} = action.payload
            state.cards = state.cards.map(c => c.id === cardId ? {
                ...c,
                model_id,
                submitSuccess: true,
                tasks: [...c.tasks, {task_id}]
            } : {...c})

        })
            .addCase(fetchCards.fulfilled, (state, action) => {
                if (!action.payload.length) {
                    return state
                }
                state.cards = action.payload
                state.nextCardId = state.nextCardId + action.payload.length
            })
            .addCase(deleteSearchCard.fulfilled, (state, action) => {
                if (typeof action.payload == 'undefined') {
                    return state
                }
                state.cards = state.cards.filter(c => c.id !== action.payload)
            })
    }
})

export const deleteSearchCard = createAsyncThunk('cards/delete', async (card_id, {
    dispatch,
    rejectWithValue,
    getState
}) => {
    const state = getState()
    const user_id = state.user.id
    const model_id = state.searchCards.cards.find(c => c.id === card_id).model_id
    console.log("card_id", card_id)
    console.log("model_id", model_id)

    if (!model_id) {
        dispatch(deleteUnSubmittedCard(card_id))
    } else {
        try {
            await api.delete('/cards', {data: {user_id, model_ids: [model_id]}})
            dispatch(notifyTemp({type: Ntypes.SUCCESS, message: `Deleted card`}))
            // dispatch(fetchCards()) if no error then the card was deleted in db, and we only filter cards in the client
            return card_id
        } catch (e) {
            rejectWithValue(e.response.json())
        }
    }
})

export const fetchCards = createAsyncThunk('cards/fetch', async (_, {dispatch, rejectWithValue, getState}) => {
    const state = getState()
    try {
        const res = await api.get('/cards', {
            params: {
                user_id: state.user.id
            },
        })
        const cards = res.data.map((c, i) => {
            let experience;
            if (c.job_board_name === 'Indeed') {
                experience = {
                    label: c.experience[0] || 'all',
                    value: c.experience[0]
                }
            } else if (c.job_board_name === 'Linkedin') {
                experience = c.experience.map(exp => ({label: exp || 'all', value: exp}))
            }
            const oldCard = {
                id: state.searchCards.nextCardId + i,
                tasks: [{task_id: c.task_id}],
                model_id: c.id,
                formValues: {
                    what: c.what,
                    where: c.where,
                    age: {label: c.age || 'all', value: c.age},
                    radius: {label: c.radius || 'all', value: c.radius},
                    job_category: {
                        label: JOB_CATEGORY_OPTIONS.find(o => o.value === c.job_category)?.label,
                        value: c.job_category
                    },
                    experience,
                },
                job_board: c.job_board_name.toLowerCase(),
                submitSuccess: true,
                isChecked: true,
            }

            if (oldCard.tasks.length > 0) {
                _subscribeTask(
                    {
                        model_id: oldCard.model_id,
                        task_id: oldCard.tasks[oldCard.tasks.length - 1].task_id
                    },
                    dispatch
                )
            }

            return oldCard // into array of cards for the redux state slice
        })
        return cards
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})

export const createTask = createAsyncThunk('tasks/create', async (
    {cardId, ...newSearch},
    {
        dispatch,
        rejectWithValue,
        getState
    }) => {
    const state = getState()
    const user_id = state.user.id
    const old_model_id = state.searchCards.cards.find(c => c.id === cardId).model_id
    if (old_model_id) {
        try {
            // replacing the contents of the old card with new search query
            await api.delete('/cards', {data: {user_id, model_ids: [old_model_id]}})
        } catch (e) {
            rejectWithValue(e.response.json())
        }
    }
    // newSearch = formValues
    try {
        const res = await api.post('/search', {...newSearch, user_id}) // res.data={task_id:string, model_id:string}
        _subscribeTask({model_id: res.data.model_id, task_id: res.data.task_id}, dispatch)
        return {
            task_id: res.data.task_id,
            model_id: res.data.model_id,
            cardId,
        }
    } catch (e) {
        rejectWithValue(e.response.json())
    }

})

function _subscribeTask({model_id, task_id}, dispatch) {
    // console.log(`begin subscribe task ${task_id}`)

    let timer
    let data
    try {
        timer = setInterval(async () => {
            data = await updateProgress(task_id)
            dispatch(updateSearchCardTaskStatus({model_id, task_id, data}))
            // dispatch(fetchResults()) // not fetching results in redux ...
            if (data.state === 'FAILURE') {
                if (data.info.includes('Linkedin account')) {
                    dispatch(notify({type: Ntypes.ERROR, message: data.info}))
                } else {
                    dispatch(notifyTemp({type: Ntypes.ERROR, message: data.info}))
                }
            }
            if (data.state === 'VERIFICATION') {
                dispatch(notify({type: Ntypes.WARNING, message: `Verification ${data.info}`}))
                console.log({task_id: data.info.task_id, email: data.info.email})
                dispatch(loginVerificationRequested({task_id: data.info.task_id, email: data.info.email}))
            }
            if (data.state === 'VERIFYING') {
                dispatch(clearNotification())
                dispatch(loginVerificationRequested(null))
            }

            const isFinished = data &&
                (data.state === 'SUCCESS'
                    || data.state === 'REVOKED'
                    || data.state === 'FAILURE'
                    || data.state === 'CLEARED')
            if (isFinished) {
                clearInterval(timer)
            }
        }, 10_000)
    } catch (e) {
        console.log(e)
        clearInterval(timer)
    }

    return timer
}


export const revokeTask = createAsyncThunk('tasks/revoke', async ({cardId, task_id}, {
    dispatch,
    rejectWithValue,
    getState
}) => {
    try {
        console.log("revoke", cardId, task_id)
        const data = await revokeSearchTask(task_id)
        dispatch(updateSearchCardTaskStatus({cardId, task_id, data}))
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})

export const {
    addSearchCard,
    updateSearchCardFormValues,
    updateSearchCardTaskStatus,
    toggledCard,
    setAllCardsChecked,
    deleteUnSubmittedCard
} = searchCardsSlice.actions

export default searchCardsSlice