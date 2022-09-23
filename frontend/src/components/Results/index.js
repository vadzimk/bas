import './main.css'
import RightPanel from "./RightPanel";
import TableWithControls from "./TableWithControls";
import {useSelector} from "react-redux";
import {useEffect, useRef, useState} from "react";

export const emptyDetail = {
    job_id: "",
    description: "",
    company_homepage_url: "",
    job_url: "",
    title: "",
    company_name: "",
    boardLogo: "",
}
export default function Results() {

    const user = useSelector(state => state.user)
    const [detail, setDetail] = useState(emptyDetail)

    // ------------------------- Draggable panel ----------------------------

    const BORDER_SIZE = 8;
    const panelRef = useRef()
    const tableContainerRef = useRef()

    useEffect(() => {
        const panel = panelRef.current
        const table_container = tableContainerRef.current

        let m_pos;

        function resize(e) {
            const dx = m_pos - e.x;
            m_pos = e.x;
            panel.style.width = (parseInt(getComputedStyle(panel, '').width) + dx) + "px";
            table_container.style.width = (parseInt(getComputedStyle(table_container, '').width) - dx) + "px";
        }

        panel.addEventListener("mousedown", function (e) {
            if (e.offsetX < BORDER_SIZE) {
                m_pos = e.x;
                document.addEventListener("mousemove", resize, false);
            }
        }, false);

        document.addEventListener("mouseup", function () {
            document.removeEventListener("mousemove", resize, false);
        }, false);
    }, [panelRef, tableContainerRef])


    if (user?.id) return (
        <div>
            <div style={{display: "flex", flexDirection: "row"}}>
                <TableWithControls
                    detail={detail}
                    setDetail={setDetail}
                    tableContainerRef={tableContainerRef}
                />
                <RightPanel
                    detail={detail}
                    panelRef={panelRef}
                />
            </div>
        </div>

    )
}