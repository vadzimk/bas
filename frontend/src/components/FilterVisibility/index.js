import React, {useEffect, useRef, useState} from 'react'
import 'react-tabulator/lib/styles.css';
import {TabulatorFull} from "tabulator-tables"; //import Tabulator library
import {useSelector, useDispatch} from 'react-redux'
import {getFilteredCompanies, unfilterCompany} from "../../services/filterVisibilityService";
import headerMenu from "../Results/TableWithControls/scripts/headerMenu";
import autoColumnsDefinitions from "../Results/TableWithControls/scripts/autoColumnDefinitions";

//https://github.com/olifolkerd/tabulator/issues/3548
// if (table.initialized){ table.setData(lData)} else {//make table}

export default function FilterVisibility() {

    const user_id = useSelector(state => state.user.id)
    const dispatch = useDispatch()
    const [data, setData] = useState([])
    const [table, setTable] = useState()
    let tableRef = useRef()
    const action = 'Filtered'
    if (data.length) {
        data[0][action] = null
    }

    useEffect(() => {
        getFilteredCompanies(user_id).then(data => {
            setData(data)
        }).catch(e => console.log(e))
    }, [user_id])

    // useEffect(() => {
    //     const table = tableRef.current
    //     if (table?.initialized) {
    //         console.log('replacing data')
    //         table.replaceData(data)
    //     } else if (table) {
    //         console.log('setting data')
    //         table.setData(data)
    //     }
    // }, [tableRef, data])

    function autoColumnsDefinitions(definitions) {
        definitions.forEach(c => {
            if (c.field.includes('url')) {
                c.formatter = (cell) => (`<a href="${cell.getValue()}" target="_blank" style="color: blue;">${cell.getValue()}</a>`)
            }
            if (c.field === 'Company_id') {
                c.visible = false
            }
            if (c.field === action) {
                c.formatter = "buttonCross"
                c.cellClick = function (e, cell) {
                    //e - the click event object
                    //cell - cell component
                    const company_id = cell.getRow().getData().Company_id
                    unfilterCompany(company_id, user_id).then(data => {
                            setData(data)
                        }
                    ).catch(e => console.log(e))

                }
            }
        })
        return definitions
    }

    const tableConfig = {
        data: data,
        index: 'Company_id',
        autoColumns: true,  // automatically make columns structure by examining the first row of the table.
        autoColumnsDefinitions: autoColumnsDefinitions,
        layout: "fitColumns",
        movableColumns: true,
        columnDefaults: {
            headerMenu: headerMenu,
            resizable: 'header',
            headerTooltip: true,
        },
    }

    useEffect(() => {
        if (table?.getData()?.length) {
            console.log("replaced data")
            table.replaceData(data)
            return
        } else if (table?.getData()) {
            console.log("table?.getData()-> set data")
            table.setData(data)
        } else {
            const aTable = new TabulatorFull(tableRef, tableConfig)
            setTable(aTable)
        }

    }, [data])


// return (
//     <div>
//         <ReactTabulator
//             onRef={(ref) => (tableRef = ref)}
//             data={data}
//             columns={columns}
//             layout={"fitColumns"}
//             movableColumns={true}
//         />
//     </div>
// )
    return <div
        ref={r => (tableRef = r)}
        // style={{height: "100%"}}
    />
}

