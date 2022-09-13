import {TextField, Button} from '@mui/material'
import React, {useEffect, useState} from "react";

import api from "../../services/api";

import BasTabulatorF from "./BasTabulatorF";
import {multiColumnFilter} from "./scripts/filter";
import table, {state} from "./scripts/table";


export default function TableWithControls() {
    const tableRef = React.useRef()

    // const valueEl = document.getElementById("filter-value");
    //
    // valueEl.addEventListener("keyup", function () {
    //     const value = valueEl.value;
    //     multiColumnFilter(value, tableRef.current)
    // })

    //Clear filter on "Clear Filters" button click
    // document.getElementById("filter-clear").addEventListener("click", function () {
    //     // valueEl.value = "";
    //     tableRef.current.clearFilter();
    // });

    // document.getElementById("reset-table-layout").addEventListener("click", function () {
    //     Object.keys(localStorage).forEach((key) => {
    //         if (key.startsWith('tabulator')) {
    //             window.localStorage.removeItem(key)
    //         }
    //     })
    // });

    // const undoDeleteButton = document.getElementById('undo-delete')
    // undoDeleteButton.addEventListener('click', function () {
    //     // http://tabulator.info/docs/5.3/history#undo
    //     // if (!state.deletedRows.length) {
    //     //     return
    //     // }
    //     // const {deletedRows} = state
    //     // const idsToUnDelete = deletedRows[deletedRows.length - 1]
    //     // unDeleteRows(idsToUnDelete)
    //     // state.deletedRows.pop()
    // })

    function unDeleteRows(jobIds) {
        // if (!jobIds) {
        //     console.log("jobIds", jobIds)
        //     return
        // }
        // const records = jobIds.map(id => ({job_id: id, job_is_deleted: false}))
        // console.log("records to undo", records)
        // api.put('/api/jobs', records)
        //     .then((res) => {
        //         tableRef.current.setData(res.data)
        //         if (!state.deletedRows.length) {
        //             undoDeleteButton.classList.remove('is-info')
        //
        //         }
        //     }).catch((e) => {
        //     console.log(e)
        // })
    }


    return (

        <div id="table-container">
            <div style={{display: "flex", justifyContent: "start", gap: "4px", margin: "8px 0"}}>
                <div>
                    <TextField
                        label="Filter"
                        size="small"
                        id="filter-value"
                    />
                </div>
                <Button
                    variant="outlined"
                    // sx={{height: "100%", width: "85px"}}
                    // disabled={formSubmitted}
                    id="filter-clear"
                    size="small"
                >
                    Clear
                </Button>
                <Button
                    id="reset-table-layout"
                    variant="outlined"
                    size="small"
                >
                    Reset Layout
                </Button>
                <Button
                    id="undo-delete"
                    variant="outlined"
                    size="small"
                >
                    Undo Delete
                </Button>
                {/*            <span>Shift+Enter to submit cell </span>*/}
            </div>
            <BasTabulatorF innerRef={tableRef}/>
        </div>
    )
}