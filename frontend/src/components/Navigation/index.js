import {Link as ReRoLink} from "react-router-dom";
import Profile from "./Profile";
import Logout from "./Logout";
import Register from "./Register";
import Login from "./Login";
import {Button, Link} from '@chakra-ui/react'

function ResultsOrTasks({pathname}) {
    return (<>
            {pathname === '/'
                ? <Button
                    style={{width: "85px"}}
                >
                    <Link
                        to="/task-results"
                        as={ReRoLink}
                    >
                        Results
                    </Link>
                </Button>
                :
                <Button
                    style={{width: "85px"}}
                >
                    <Link
                        to="/"
                        as={ReRoLink}
                    >
                        Tasks
                    </Link>
                </Button>
            }
        </>
    )
}

export default function Navigation({user, pathname}) {
    return (
        <div style={{display: 'flex', gap: "4px", margin: "8px 0"}}>
            {user.id ?
                <>
                    <ResultsOrTasks pathname={pathname}/>
                    <Profile/>
                    <Logout/>
                </>
                :
                <>
                    <Register/>
                    <Login/>
                </>
            }
        </div>
    )
}