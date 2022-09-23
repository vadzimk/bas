import {userLoggedIn} from "../../reducers/userSlice";
import {notify, Ntypes} from "../../reducers/notificationSlice";
import {addSearchCard, deleteSearchCard} from "../../reducers/searchCardsSlice";
import {SearchCard} from "./SearchCard";
import {SearchCardContext} from "../../App";
import {Button, Stack, Checkbox} from "@chakra-ui/react";
import {useSelector, useDispatch} from "react-redux";
import {useEffect} from "react";
import {SearchIcon} from "@chakra-ui/icons"


export default function Tasks() {
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
                // maxWidth: "600px",
                padding: "0 32px",
                margin: "0px auto",
                display: 'flex',
                flexDirection: 'column',
                // gap: "10px 0"
            }}>

            <div style={{display: 'flex', gap: "4px"}}>

                {user.id && <>
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
                </>}
            </div>
            <div style={{marginTop: "16px"}}>
                <Checkbox
                    defaultChecked
                    // onChange={} // TODO select all cards
                    size="lg"
                    borderColor="#0088CC"
                    style={{height: "55px"}}
                ></Checkbox>
                <Stack>
                    {user.id && cards.map(card =>
                        <SearchCardContext.Provider value={{
                            cardId: card.id,
                            onDelete: () => handleSearchCardDelete(card.id),
                            platform: card.job_board,
                        }} key={card.id}>
                            <SearchCard/>
                        </SearchCardContext.Provider>
                    )}
                </Stack>
            </div>
        </div>
    )
}