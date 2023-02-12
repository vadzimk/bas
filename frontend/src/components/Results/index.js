import './main.css'
import RightPanel from "./RightPanel";
import TableWithControls from "./TableWithControls";
import {useSelector} from "react-redux";
import {useState} from "react";
import {Panel, PanelGroup, PanelResizeHandle} from "react-resizable-panels";

export const emptyDetail = {
    job_id: "",
    description: "",
    company_homepage_url: "",
    job_url: "",
    title: "",
    company_name: "",
    boardLogo: "",
}
export default function Results({getData, updateRow}) {

    const user = useSelector(state => state.user)
    const [detail, setDetail] = useState(emptyDetail)

    // ------------------------- Resizable panels ----------------------------


    if (user?.id) return (
        <PanelGroup direction="horizontal"
                    style={{minHeight: "80vh"}}
        >
            <Panel defaultSize={70} minSize={25}>
                <TableWithControls
                    detail={detail}
                    setDetail={setDetail}
                    getData={getData}
                    updateRow={updateRow}
                />
            </Panel>
            <PanelResizeHandle style={{width: "8px", backgroundColor: "#ffffff"}}/>
            <Panel defaultSize={30} minSize={1}>
                <RightPanel
                    detail={detail}
                />
            </Panel>
        </PanelGroup>
    )
}