import {userLoggedIn} from "../../reducers/userSlice";
import {notify, Ntypes} from "../../reducers/notificationSlice";
import {addSearchCard, deleteSearchCard} from "../../reducers/searchCardsSlice";
import {SearchCard} from "../SearchCard";
import {SearchCardContext} from "../../App";
import {Button} from "@mui/material";
import {useTheme, css} from "@emotion/react";
import {useSelector, useDispatch} from "react-redux";
import {useEffect} from "react";


export default function Tasks() {
    const theme = useTheme()
    const cards = useSelector(state => state.searchCards.cards)
    const user = useSelector(state => state.user)

    const dispatch = useDispatch();
    useEffect(() => {
        const user = JSON.parse(window.localStorage.getItem('bas-user')) // TODO persist the whole user object
        if (user?.id) {
            dispatch(userLoggedIn(user))
        }
    }, [])

    const handleNewSearchCardLinkedin = () => {
        if (!user.linkedin_credentials) {
            dispatch(notify({type: Ntypes.ERROR, message: 'Linkedin credentials are missing, please UPDATE USER'}))
            return
        }
        dispatch(addSearchCard('linkedin'))
    }

    const handleNewSearchCardIndeed = () => {
        dispatch(addSearchCard('indeed'))
    }

    const handleSearchCardDelete = (id) => {
        dispatch(deleteSearchCard(id))
    }


    return (
        <div
            style={{
                maxWidth: "1600px",
                margin: "0 auto",

            }}>

            <h3 style={theme.typography.h4}>Tasks</h3>
            <div style={{display: 'flex', gap: "4px"}}>

                {user.id && <Button
                    variant="outlined"
                    onClick={handleNewSearchCardLinkedin}>
                    Linkedin Search
                </Button>}
                {user.id && <Button
                    variant="outlined"
                    onClick={handleNewSearchCardIndeed}>
                    Indeed Search
                </Button>}
            </div>
            <div>
                {user.id && cards.map(card =>
                    <SearchCardContext.Provider value={{
                        cardId: card.id,
                        onDelete: () => handleSearchCardDelete(card.id),
                        platform: card.job_board,
                    }} key={card.id}>
                        <SearchCard/>
                    </SearchCardContext.Provider>
                )}
            </div>
        </div>
    )
}