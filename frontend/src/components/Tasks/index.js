import {userLoggedIn} from "../../reducers/userSlice";
import {notify, Ntypes} from "../../reducers/notificationSlice";
import {addSearchCard, deleteSearchCard, setAllCardsChecked} from "../../reducers/searchCardsSlice";
import {SearchCard} from "./SearchCard";
import {SearchCardContext} from "../../App";
import {Button, Stack, Checkbox} from "@chakra-ui/react";
import {useSelector, useDispatch} from "react-redux";
import {useEffect} from "react";
import {SearchIcon} from "@chakra-ui/icons"


export default function Tasks() {
    const cards = useSelector(state => state.searchCards.cards)
    const user = useSelector(state => state.user)

    const checkedItems = cards.map(c => c.isChecked)
    const allChecked = checkedItems.every(Boolean)
    const isIndeterminate = checkedItems.some(Boolean) && !allChecked

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

    const handleToggleAllCards = (e) => {
        dispatch(setAllCardsChecked(e.target.checked))
    }

    console.log("cards", cards)

    if (user.id)
        return (
            <div
                style={{
                    // maxWidth: "600px",
                    padding: "0 32px",
                    margin: "0px auto",
                    display: 'flex',
                    flexDirection: 'column',
                    // gap: "10px 0"
                }}>

                <div style={{display: 'flex', gap: "4px"}}>

                    <Button
                        rightIcon={<SearchIcon/>}
                        variant="outline"
                        onClick={handleNewSearchCardLinkedin}>
                        New Linkedin
                    </Button>
                    <Button
                        rightIcon={<SearchIcon/>}
                        variant="outline"
                        onClick={handleNewSearchCardIndeed}>
                        New Indeed
                    </Button>

                </div>
                {cards.length > 0 &&
                    <div style={{marginTop: "16px"}}>
                        <Checkbox
                            isChecked={allChecked}
                            isIndeterminate={isIndeterminate}
                            onChange={handleToggleAllCards}
                            size="lg"
                            borderColor="#0088CC"
                            style={{height: "55px"}}
                        ></Checkbox>
                        <Stack>
                            {[...cards]
                                .sort((a, b) => a.formValues.what.localeCompare(b.formValues.what))
                                .map(card =>
                                    <SearchCardContext.Provider value={{
                                        cardId: card.id,
                                        onDelete: () => handleSearchCardDelete(card.id),
                                        platform: card.job_board,
                                    }} key={card.id}>
                                        <SearchCard/>
                                    </SearchCardContext.Provider>
                                )}
                        </Stack>
                    </div>}
            </div>
        )
}