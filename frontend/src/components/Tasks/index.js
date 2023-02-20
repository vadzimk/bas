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
    const handleNewSearchCardBuiltin = () => {
        dispatch(addSearchCard('builtin'))
    }
    const handleSearchCardDelete = (id) => {
        dispatch(deleteSearchCard(id))
    }

    const handleToggleAllCards = (e) => {
        dispatch(setAllCardsChecked(e.target.checked))
    }


    if (user.id)
        return (
            <div
                style={{
                    // maxWidth: "600px",
                    padding: "0 16px",
                    margin: 0,
                    display: 'flex',
                    flexDirection: 'column',
                    // gap: "10px 0"
                }}>
                {cards.length > 0 &&
                    <div>
                        <div style={{display: 'flex', gap: "4px", margin: "8px 0"}}>
                            <Checkbox
                                isChecked={allChecked}
                                isIndeterminate={isIndeterminate}
                                onChange={handleToggleAllCards}
                                size="lg"
                                borderColor="#0088CC"
                                style={{marginRight: "42px"}}
                            ></Checkbox>
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
                            <Button
                                rightIcon={<SearchIcon/>}
                                variant="outline"
                                onClick={handleNewSearchCardBuiltin}>
                                New Builtin
                            </Button>

                        </div>
                        <Stack>
                            {[...cards]
                                .sort((a, b) => (a.formValues?.what ? a.formValues.what.localeCompare(b.formValues.what) : 0))
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