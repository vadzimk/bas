import "tabulator-tables/dist/css/tabulator.min.css";
import {ReactTabulator} from 'react-tabulator'

import React, {useCallback, useEffect, useState} from "react";
import {getAllResults} from "../../services/resultService";
import {useSelector} from 'react-redux'
import autoColumnsDefinitions from "./scripts/autoColumnDefinitions";

export default function BasTabulator() {
    let innerRef = React.useRef()

    const {id: userId} = useSelector(state => state.user)
    const [data, setData] = useState([])

    const getData = useCallback(async () => {
        try {
            const data = await getAllResults()
            setData(data)
        } catch (e) {
            console.log(e)
        }
    }, [userId])

    useEffect(() => {
        getData()
    }, [getData])

    console.log("table", innerRef)

    const rowClick = (e, row) => {
        console.log('ref table: ', innerRef.current); // this is the Tabulator table instance

    };
    if (data.length) return (
        <ReactTabulator
            onRef={(r) => (innerRef = r)}
            maxHeight="80vh"
            index="job_id" //set the index field
            data={data}
            // columns={[{title: "job_id", field: "job_id"}]}
            events={{
                rowClick: rowClick
            }}
            autoColumns={true}  // automatically make columns structure by examining the first row of the table.
            // autoColumnsDefinitions={autoColumnsDefinitions}
            // resizableColumnFit={false}
            // history={true}
            // layout="fitColumns"  //  the table will resize columns so that they fit inside the width of the container.
            // movableColumns={true}
            // persistence={true} //enable table persistence
            // persistenceMode="local" //store persistence information in local storage
            // clipboard={true} //enable clipboard functionality
            // responsiveLayout="collapse" // collapse columns that no longer fit on the table into a list under the row
            // selectable={true}  // enable row selection
            // validationMode="manual" // no vaildation is automatically performed on edit
            // columnDefaults={{
            //     tooltip: makeToolTipFunction(), //TODO uncomment this~!
            //     editor: "input",
            //     headerMenu: headerMenu,
            //     resizable: 'header',
            //     headerTooltip: true,
            //     download: true,  // include hidden columns in the download
            //     contextMenu: cellMenu,
            // }}

        />
    )
}