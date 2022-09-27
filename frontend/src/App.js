import React, {createContext, useEffect,} from 'react';
import {useSelector, useDispatch} from "react-redux";
import {userLoggedIn} from "./reducers/userSlice";


import Tasks from "./components/Tasks";
import Results from "./components/Results";
import UserHub from "./components/UserHub";

import {Alert, AlertIcon, Text} from '@chakra-ui/react'
import {Tabs, TabList, TabPanels, Tab, TabPanel} from '@chakra-ui/react'
import {fetchResults} from "./reducers/resultsSlice";
import {fetchCards} from "./reducers/searchCardsSlice";
import {PlanApply} from "./components/PlanApply";
import {getResults, updateResultsRow} from "./services/resultService";

export const SearchCardContext = createContext({
    cardId: null,
    onDelete: null,
    platform: null
})

function App() {

    const user = useSelector(state => state.user)
    const notification = useSelector(state => state.notification)
    const dispatch = useDispatch();


    useEffect(() => {
        const user = JSON.parse(window.localStorage.getItem('bas-user'))
        if (user?.id) {
            dispatch(userLoggedIn(user))
        }
    }, [])

    useEffect(() => {
        dispatch(fetchCards())
    }, [user?.id])


    return (
        <div style={{position: "relative"}}>
            <div style={{height: "100px", backgroundColor: "#d6e4ea"}}/>
            <div style={{position: "absolute", top: 0, left: 0, width: "100%"}}>
                <Tabs variant='solid-rounded' isLazy={true}>
                    <div style={{
                        maxWidth: "1600px",
                        margin: "0 auto",
                        padding: "0 32px",
                        display: "flex",
                        flexDirection: "column"
                    }}>
                        {notification.type &&
                            <Alert rounded="base"
                                   status={notification.type}
                                   style={{
                                       zIndex: "999999",
                                       position: "fixed",
                                       justifyContent: "center",
                                       alignSelf: "center",
                                       width: "auto"
                                   }}
                            >
                                <AlertIcon/>
                                {notification.message}
                            </Alert>
                        }
                        <div style={{
                            display: 'flex', justifyContent: 'space-between'
                        }}>
                            <div style={{
                                height: "100px",
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-between",
                                flexShrink: 0,
                            }}>
                                <Text fontSize="3xl">
                                    Blanket Application Strategy
                                </Text>
                                {user.id &&
                                    <TabList mb={2}>
                                        <Tab mr={3}>Tasks</Tab>
                                        <Tab mr={3}>Results</Tab>
                                        <Tab mr={3}>Plan Apply</Tab>
                                        <Tab mr={3}>Did Apply</Tab>
                                    </TabList>}
                            </div>
                            <div style={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'flex-end',
                            }}>
                                <UserHub/>
                            </div>
                        </div>
                    </div>
                    <TabPanels>
                        <TabPanel style={{display: "flex"}}>
                            <Tasks/>
                        </TabPanel>
                        <TabPanel>
                            <Results
                                getData={getResults}
                                updateRow={updateResultsRow}
                            />
                        </TabPanel>
                        <TabPanel>
                            <PlanApply/>
                        </TabPanel>
                        <TabPanel>
                            <Results
                                getData={getResults}
                                updateRow={updateResultsRow}
                            />
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </div>
        </div>
    )
}


export default App;
