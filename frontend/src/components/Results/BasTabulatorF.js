import "tabulator-tables/dist/css/tabulator.min.css";
import {TabulatorFull} from "tabulator-tables"; //import Tabulator library

import React, {useEffect, useState} from "react";
import {getAllResults} from "../../services/resultService";
import {useSelector} from 'react-redux'
import autoColumnsDefinitions from "./scripts/autoColumnDefinitions";
import makeToolTipFunction from "./scripts/tooltip";
import headerMenu from "./scripts/menus/headerMenu";
import cellMenu from "./scripts/menus/cellMenu";
import attachDetail from "./scripts/attachDetail";
import api from "../../services/api";


export default function BasTabulatorF({innerRef}) {

    const {id: userId} = useSelector(state => state.user)
    const [data, setData] = useState([])
    let table

    useEffect(() => {
       getAllResults().then(data=>{
           setData(data)
       }).catch(e=>console.log(e))
    }, [])

    useEffect(() => {
        const tableConfig = {
            maxHeight: "80vh",
            index: "job_id", //set the index field
            data: data,
            autoColumns: true,  // automatically make columns structure by examining the first row of the table.
            autoColumnsDefinitions: autoColumnsDefinitions,
            resizableColumnFit: false,
            debugInvalidOptions: false,
            history: true,
            layout: "fitColumns",  //  the table will resize columns so that they fit inside the width of the container.
            movableColumns: true,
            persistence: true, //enable table persistence
            persistenceMode: "local", //store persistence information in local storage
            clipboard: true, //enable clipboard functionality
            responsiveLayout: "collapse", // collapse columns that no longer fit on the table into a list under the row
            selectable: true,  // enable row selection
            validationMode: "manual", // no vaildation is automatically performed on edit
            columnDefaults: {
                // tooltip: makeToolTipFunction(),
                editor: "input",
                headerMenu: headerMenu,
                resizable: 'header',
                headerTooltip: true,
                download: true,  // include hidden columns in the download
                contextMenu: cellMenu,
            },
        }
        table = new TabulatorFull(innerRef, tableConfig)
        attachTableEventListeners()

    }, [data])

    function attachTableEventListeners() {
        let currentRowElement;

        function highlightCurrentRowElement(row) {
            if (currentRowElement) {
                currentRowElement.classList.remove('current-row')
            }
            currentRowElement = row.getElement()
            currentRowElement.classList.add('current-row')
        }

// TODO detach detail when no row selected
        table.on('rowClick', function (e, row) {
            attachDetail(row)
            highlightCurrentRowElement(row)
        })

        table.on("cellEditing", function (cell) {
            const row = cell.getRow()
            attachDetail(row)
            highlightCurrentRowElement(row)
        });

        table.on('cellEdited', function (cell) {
            const job_id = cell.getRow().getData().job_id
            const oldValue = cell.getOldValue()
            const newValue = cell.getValue()
            if (
                ([null, ""].includes(oldValue) && [null, ""].includes(newValue))
                || oldValue?.toString().trim() === newValue?.toString().trim()) {  // no change in cell value
                return
            }
            console.log("updating", JSON.stringify(oldValue), typeof oldValue, "=>", JSON.stringify(newValue), typeof newValue)
            const column = cell.getField()
            const recordToSend = {
                job_id,
                [column]: newValue
            }
            if (!recordToSend.job_id) {
                return
            }
            // TODO this causes the table to crash often, because it resets data while editing
            api.put('/job', recordToSend)
                .then(res => {
                    table.setData(res.data);
                    // restoreColumnLayout()
                })
                .catch(e => console.log(e))

        })
    }

    console.log("table", innerRef)

    const rowClick = (e, row) => {
        console.log('ref table: ', innerRef.current); // this is the Tabulator table instance

    };
    return <div ref={r => (innerRef = r)}/>
}