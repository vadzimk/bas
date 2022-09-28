import {getResults, updateResultsRow} from "../services/resultService";
import {createAsyncThunk, createSlice} from "@reduxjs/toolkit"


const initialState = {
    data: [],
    deletedRecords: [],
    updatedRecordsOldValues: [],
}

const resultsSlice = createSlice({
    name: "results",
    initialState,
    reducers: {
        saveOldRecord: function (state, action) {
            state.updatedRecordsOldValues = [...state.updatedRecordsOldValues, action.payload]
        },
        undoneLastUpdate: function(state, action){
            state.updatedRecordsOldValues = state.updatedRecordsOldValues.slice(0, -1)
        }
    },
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
        return await updateResultsRow(recordToSend)
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})

export const undoUpdateResults = createAsyncThunk('results/undoUpdateResults', async (_, {
    dispatch,
    rejectWithValue,
    getState
}) => {
    try {
        const state = getState()
        const record = state.results.updatedRecordsOldValues[state.results.updatedRecordsOldValues.length - 1]
        const model_ids = state.searchCards.cards
            .filter(c => c.isChecked === true)
            .map(c => c.model_id)
        const user_id = state.user.id
        const res_data = await updateResultsRow(record, model_ids, user_id)
        dispatch(undoneLastUpdate)
        return res_data
    } catch (e) {
        rejectWithValue(e.response.json())
    }
})

export const {
    saveOldRecord,
    undoneLastUpdate,
} = resultsSlice.actions

export default resultsSlice