import {createAsyncThunk, createSlice} from "@reduxjs/toolkit"
import api from "../services/api";


const initialState = {
    cards: [],
    nextCardId: 0,

}

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
                jobBoard: action.payload
            }
            state.cards = [...state.cards, newCard]
            state.nextCardId = state.nextCardId + 1
        },
        deleteSearchCard: function (state, action) {
            state.cards = state.cards.filter(c => c.id !== action.payload)
        }
    },
    extraReducers: builder => {
        builder.addCase(createTask.fulfilled, (state, action) => {
            const {task_id, model_id, cardId} = action.payload
            state.cards = state.cards.map(c=>c.id===cardId
                ? {...c,
                    model_id,
                    tasks: [...c.tasks, {task_id} ]}
                : {...c})

        })
    }
})

export const createTask = createAsyncThunk('tasks/create', async (
    {cardId, ...newSearch},
    {
        dispatch, rejectWithValue,
        getState
    }) => {
    // newSearch = formValues
    // TODO need to have the id of the card here
    const state = getState()
    try {
        const res = await api.post('/search', {...newSearch, user_id: state.user.id})
        return {task_id: res.data.task_id, model_id: res.data.model_id, cardId} // res.data={task_id:string, model_id:string}
    } catch (e) {
        rejectWithValue(e.response.json())
    }

})

export const {addSearchCard, deleteSearchCard} = searchCardsSlice.actions
export default searchCardsSlice.reducer