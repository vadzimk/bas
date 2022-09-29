import React, {useEffect, useRef, useState} from 'react'
import 'react-tabulator/lib/styles.css';
import {ReactTabulator} from 'react-tabulator'
import {useSelector, useDispatch} from 'react-redux'
import {getFilteredCompanies, unfilterCompany} from "../../services/filterVisibilityService";
import headerMenu from "../Results/TableWithControls/scripts/headerMenu";

//https://github.com/olifolkerd/tabulator/issues/3548
// if (table.initialized){ table.setData(lData)} else {//make table}

export default function FilterVisibility() {

    const user_id = useSelector(state => state.user.id)
    const dispatch = useDispatch()
    const [data, setData] = useState([])
    let tableRef = useRef()

    useEffect(() => {
        getFilteredCompanies(user_id).then(data => {
            setData(data)
        }).catch(e => console.log(e))
    }, [user_id])

    useEffect(()=>{
        const table = tableRef.current
        if(table?.initialized){
            console.log('replacing data')
            table.replaceData(data)
        } else if (table){
            console.log('setting data')
            table.setData(data)
        }
    }, [tableRef, data])

    if (data.length) {
        const columnDefaults = {
            headerMenu: headerMenu,
            resizable: 'header',
            headerTooltip: true,
        }
        const columns = Object.keys(data[0]).concat(['Action'])
            .map(c => ({field: c, title: c, ...columnDefaults}))
        columns.forEach(c => {
            if (c.field.includes('url')) {
                c.formatter = (cell) => (`<a href="${cell.getValue()}" target="_blank" style="color: blue;">${cell.getValue()}</a>`)
            }
            if (c.field === 'Company_id') {
                c.visible = false
            }
            if(c.field === 'Action'){
                c.formatter = "buttonCross"
                c.cellClick = function (e, cell) {
                    //e - the click event object
                    //cell - cell component
                    const company_id = cell.getRow().getData().Company_id
                    unfilterCompany(company_id, user_id).then(data=> {
                            // const table = cell.getRow().getTable()
                            setData(data)
                        }
                    ).catch(e=>console.log(e))

                }
            }
        })
        return (
            <div>
                <ReactTabulator
                    onRef={(ref) => (tableRef = ref)}
                    data={data}
                    columns={columns}
                    layout={"fitColumns"}
                    movableColumns={true}
                />
            </div>
        )
    }
}