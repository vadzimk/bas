import './main.css'
import RightPanel from "./RightPanel";
import TableWithControls from "./TableWithControls";
import {useSelector} from "react-redux";

export default function Results() {
    const user = useSelector(state => state.user)
    if (user?.id) return (
        <div>
            <div style={{display: "flex", flexDirection: "row"}}>
                <TableWithControls/>
                <RightPanel/>
            </div>
        </div>

    )
}