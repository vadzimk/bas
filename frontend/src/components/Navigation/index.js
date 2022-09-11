import {Link} from "react-router-dom";
import Profile from "../Profile";
import Logout from "../Logout";
import Register from "../Register";
import Login from "../Login";
import {Button} from "@mui/material";

function ResultsOrTasks({pathname}) {
    return (<>
            {pathname === '/'
                ? <Button
                    component={Link}
                    to="/task-results"
                    variant="outlined"
                    sx={{width: "85px"}}
                >
                    Results
                </Button>
                :
                <Button
                    component={Link}
                    to="/"
                    variant="outlined"
                    sx={{width: "85px"}}

                >
                    Tasks
                </Button>
            }
        </>
    )
}

export default function Navigation({user, pathname}) {
    return (
        <div style={{display: 'flex', gap: "4px"}}>
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