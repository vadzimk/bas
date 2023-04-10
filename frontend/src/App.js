import React, {createContext, useEffect,} from 'react';
import {useSelector, useDispatch} from "react-redux";
import {loginUser, userLoggedIn} from "./reducers/userSlice";


import Tasks from "./components/Tasks";
import Results from "./components/Results";
import UserHub from "./components/UserHub";

import {Alert, AlertIcon, Text} from '@chakra-ui/react'
import {Tabs, TabList, TabPanels, Tab, TabPanel} from '@chakra-ui/react'
import {fetchCards} from "./reducers/searchCardsSlice";
import {PlanApply} from "./components/PlanApply";
import {getResults, updateResultsRow} from "./services/resultService";
import {DidApply} from "./components/DidApply";
import CompanyFilterVisibility from "./components/CompanyFilterVisibility";
import {VerificationDialogue} from "./components/Verification/VerificationDialogue";


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
    }, [dispatch])

    useEffect(() => {
        dispatch(fetchCards())
    }, [user?.id, dispatch])


    return (
        <div style={{position: "relative"}}>
            <div style={{height: "70px", backgroundColor: "#d6e4ea"}}/>
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
                        {
                            <VerificationDialogue
                                isOpen={Boolean(user.login_verification_request)}
                            />
                        }
                        <div style={{
                            display: 'flex', justifyContent: 'space-between'
                        }}>
                            <div style={{
                                height: "70px",
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-between",
                                flexShrink: 0,
                            }}>
                                <Text fontSize="xl">
                                    Blanket Application Strategy
                                </Text>
                                {user.id &&
                                    <TabList mb={2}>
                                        <Tab mr={3}>Tasks</Tab>
                                        <Tab mr={3}>Results</Tab>
                                        <Tab mr={3}>Plan Apply</Tab>
                                        <Tab mr={3}>Did Apply</Tab>
                                        <Tab mr={3}>Company Visibility</Tab>
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
                        <TabPanel style={{
                            display: "flex",
                            maxWidth: "1600px",
                            margin: "0 auto",
                            padding: "0 32px",
                        }}>
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
                            <DidApply/>
                        </TabPanel>
                        <TabPanel>
                            <CompanyFilterVisibility/>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </div>
        </div>
    )
}


export default App;
