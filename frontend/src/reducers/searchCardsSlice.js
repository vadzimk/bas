import {createAsyncThunk, createSlice} from "@reduxjs/toolkit"
import api from "../services/api";
import {revokeSearchTask, updateProgress} from "../services/searchService";
import {notify, notifyTemp, Ntypes} from "./notificationSlice";


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
        deleteSearchCard: function (state, action) {
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
            const {cardId, task_id, data} = action.payload
            const computeProgress = (data) => {
                if (data.state === 'PROGRESS') {
                    return 100 * data.info.current / data.info.total
                } else if (data.state === 'SUCCESS') {
                    return 100
                } else return undefined
            }
            const progress = computeProgress(data)
            state.cards = state.cards.map(c => {
                if (c.id === cardId) {
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
    }
})

export const createTask = createAsyncThunk('tasks/create', async (
    {cardId, ...newSearch},
    {
        dispatch,
        rejectWithValue,
        getState
    }) => {
    // newSearch = formValues
    const state = getState()
    try {
        const res = await api.post('/search', {...newSearch, user_id: state.user.id}) // res.data={task_id:string, model_id:string}
        _subscribeTask({cardId, task_id: res.data.task_id}, dispatch)
        return {
            task_id: res.data.task_id,
            model_id: res.data.model_id,
            cardId,
        }
    } catch (e) {
        rejectWithValue(e.response.json())
    }

})

function _subscribeTask({cardId, task_id}, dispatch) {
    let timer
    let data
    try {
        timer = setInterval(async () => {
            data = await updateProgress(task_id)
            dispatch(updateSearchCardTaskStatus({cardId, task_id, data}))
            if (data.state === 'FAILURE') {
                if (data.info.includes('Linkedin account')) {
                    dispatch(notify({type: Ntypes.ERROR, message: data.info}))
                } else {
                    dispatch(notifyTemp({type: Ntypes.ERROR, message: data.info}))
                }
            }

            const isFinished = data &&
                (data.state === 'SUCCESS' || data.state === 'REVOKED' || data.state === 'FAILURE')
            if (isFinished) {
                clearInterval(timer)
            }
        }, 5000)

    } catch (e) {
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
    deleteSearchCard,
    updateSearchCardFormValues,
    updateSearchCardTaskStatus,
    toggledCard,
    setAllCardsChecked
} = searchCardsSlice.actions

export default searchCardsSlice.reducer