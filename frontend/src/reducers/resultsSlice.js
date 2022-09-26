import {getResults, updateRow} from "../services/resultService";
import {createAsyncThunk, createSlice} from "@reduxjs/toolkit"


const initialState = {
    data: []
}

const resultsSlice = createSlice({
    name: "results",
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder.addCase(fetchResults.fulfilled, (state, action) => {
            state.data = [...action.payload]
        })
            .addCase(updateData.fulfilled, (state, action) => {
                state.data = [...action.payload]
            })
    }
})

export const fetchResults = createAsyncThunk('results/fetch', async (_, {
    dispatch,
    rejectWithValue,
    getState
}) => {
    const state = getState()
    const model_ids = state.searchCards.cards
        .filter(c => c.isChecked === true)
        .map(c => c.model_id)
    const user_id = state.user.id
    try {
        return await getResults(model_ids, user_id)
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})

export const updateData = createAsyncThunk('results/update', async (recordToSend, {
    dispatch,
    rejectWithValue,
    getState
}) => {
    try {
        return await updateRow(recordToSend)
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})


export default resultsSlice