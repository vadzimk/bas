import {createSlice} from "@reduxjs/toolkit"


const initialState = {
    cards: [],
    nextCardId: 0

}

const searchCardsSlice = createSlice({
    name: "tasks",
    initialState,
    reducers: {
        addSearchCard: function (state, action) {
            state.cards = [...state.cards, {id: state.nextCardId}]
            state.nextCardId = state.nextCardId + 1
        },
        deleteSearchCard: function (state, action) {
            state.cards = state.cards.filter(c => c.id !== action.payload)
        }
    }
})


export const {addSearchCard, deleteSearchCard} = searchCardsSlice.actions
export default searchCardsSlice.reducer