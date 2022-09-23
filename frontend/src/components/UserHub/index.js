import Profile from "./Profile";
import Logout from "./Logout";
import Register from "./Register";
import Login from "./Login";
import {useSelector} from "react-redux"



export default function UserHub() {
    const user = useSelector(state => state.user)
    return (
        <div style={{display: 'flex', gap: "4px", margin: "8px 0"}}>
            {user.id ?
                <>
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