import {Input, Button} from '@chakra-ui/react'
import React, {useEffect, useState} from "react";
import api from "../../../services/api";
import BasTabulator from "./BasTabulatorF";
import {emptyDetail} from "../index";
import {useSelector, useDispatch} from "react-redux"
import {saveOldRecord, undoneLastUpdate, undoUpdateResults} from "../../../reducers/resultsSlice";
import {updateResultsRow} from "../../../services/resultService";
import {loginUser} from "../../../reducers/userSlice";


export default function TableWithControls({detail, setDetail, tableContainerRef, getData, updateRow}) {
    const [table, setTable] = useState()
    const [filterValue, setFilterValue] = useState("")
    const [deletedRows, setDeletedRows] = useState([]) // array of arrays (each deletion pushes an array)
    const {updatedRecordsOldValues} = useSelector(state => state.results)
    const state = useSelector(state => state)
    const dispatch = useDispatch()

    useEffect(() => {
        if (table) {
            const isDetailInTable = Boolean(table.getRows().find(r => r.getData().Job_id === detail.job_id))
            if (!isDetailInTable) {
                setDetail(emptyDetail)
            }
        }
    })

    function handleFilterValueChange(e) {
        console.log("filter-value", e.target.value)
        setFilterValue(e.target.value)
        multiColumnFilter(e.target.value, table)
    }

    function multiColumnFilter(value, table) {
        const filters = [];
        if (!value) {
            table.clearFilter()
            return
        }
        const columns = table.getColumns();

        columns
            .filter(c => !c.getField().includes('url'))
            .forEach(function (column) {
                filters.push({
                    field: column.getField(),
                    type: "like",
                    value: value,
                });
            });

        table.setFilter([filters]);
    }

    function handleClearFilter() {
        table.clearFilter();
        setFilterValue("")
    }

    async function handleUndoUpdate() {
        try {
            const record = state.results.updatedRecordsOldValues[state.results.updatedRecordsOldValues.length - 1]
            const model_ids = state.searchCards.cards
                .filter(c => c.isChecked === true)
                .map(c => c.model_id)
            const user_id = state.user.id
            const res_data = await updateResultsRow(record, model_ids, user_id)
            // TODO need to pop the last value from updatedRecordsOldValues !!!! but need redux for it
            table.updateData(res_data);
            // table.replaceData(res_data);
            dispatch(undoneLastUpdate())

        } catch (e) {
            console.log(e)
        }


    }

    function handleUndoDelete() {
        // http://tabulator.info/docs/5.3/history#undo
        if (!deletedRows.length) {
            return
        }
        const idsToUnDelete = deletedRows[deletedRows.length - 1]
        unDeleteRows(idsToUnDelete) // TODO change to as a result from api call
        setDeletedRows(deletedRows.slice(0, -1)) // remove last
    }

    function unDeleteRows(jobIds) {
        if (!jobIds) {
            console.log("jobIds", jobIds)
            return
        }
        const records = jobIds.map(id => ({job_id: id, job_is_deleted: false}))
        console.log("records to undo", records)
        api.put('/jobs', records)
            .then((res) => {
                table.setData(res.data)
            }).catch((e) => {
            console.log(e)
        })
    }

// ---------------------- CellMenu ---------------------

    const cellMenu = [
        {
            label: "<i class=\"fa-solid fa-filter\"></i> Filter By Cell Value",
            action: function (e, cell) {
                const table = cell.getRow().getTable()
                const value = cell.getValue()
                setFilterValue(value)

                multiColumnFilter(value, table)
                if (!value) {
                    table.clearFilter()
                }

                // const column = cell.getColumn()
                // const filters = []
                // filters.push({
                //     field: column.getField(),
                //     type: "like",
                //     value: value,
                // });
                // table.setFilter([filters]);
            }
        },
        {
            label: "<i class=\"fa-solid fa-circle-check\"></i> Toggle Select Row",
            action: function (e, cell) {
                const row = cell.getRow()
                row.toggleSelect();
            }
        },
        {
            label: "<i class=\"fa-solid fa-check-double\"></i> Select Visible Rows",
            action: function (e, cell) {
                const table = cell.getRow().getTable()
                table.selectRow('visible')
            }
        },
        {
            label: "<i class=\"fa-solid fa-minus\"></i> Deselect All Rows",
            action: function (e, cell) {
                const table = cell.getRow().getTable()
                table.deselectRow(table.getSelectedRows());
            }
        },
        {
            separator: true,
        },
        {
            label: "<i class=\"fa-solid fa-ban\"></i> Filter Company",
            action: function (e, cell) {
                const job_id = cell.getRow().getData().Job_id
                console.log("job_id", job_id)
                api.put('/job/company/ignore', {job_id, user_id: state.user.id})
                    .then((res) => {
                            const checkedModels = state.searchCards.cards.filter(c => c.isChecked === true).map(c => c.model_id).filter(id => id != null)

                            getData(checkedModels, state.user.id)
                                .then(data => {
                                    const table = cell.getRow().getTable()
                                    table.replaceData(data)  // TODO see if it works
                                }).catch(e => console.log(e))
                        }
                    ).catch(e=>console.log(e))
            }
        },
        {
            separator: true,
        },
        {
            label: "<i class=\"fa-solid fa-trash-arrow-up\"></i> Delete Row In Focus",
            action: function (e, cell) {
                const row = cell.getRow()
                const id = row.getData().Job_id
                api.delete('/job', {data: [id]})
                    .then((res) => {
                        row.delete();
                        setDeletedRows([...deletedRows, [id]])
                    }).catch((e) => {
                    console.log(e)
                })
            }
        },
        {
            label: "<i class=\"fa-solid fa-trash-can\"></i> Delete Selected Rows",
            action: function (e, cell) {
                const table = cell.getRow().getTable()
                const selectedRows = table.getSelectedRows();
                if (!selectedRows.length) {
                    return
                }
                const ids = selectedRows.map((r) => r.getData().Job_id)
                api.delete('/job', {data: ids})
                    .then((res) => {
                        selectedRows.forEach(row => row.delete())
                        setDeletedRows([...deletedRows, ids])
                    }).catch((e) => {
                    console.log(e)
                })
            }
        },

    ]

    // --------------------------------------------

    return (

        <div id="table-container" ref={tableContainerRef}>
            <div style={{display: "flex", justifyContent: "start", gap: "4px", marginBottom: "8px"}}>
                <div>
                    <Input
                        placeholder="Filter"
                        size="sm"
                        id="filter-value"
                        borderRadius="base"
                        onChange={handleFilterValueChange}
                        value={filterValue}
                    />
                </div>
                <Button
                    variant="outline"
                    sx={{width: "114px"}}
                    id="filter-clear"
                    size="sm"
                    onClick={handleClearFilter}
                >
                    Clear
                </Button>
                <Button
                    id="undo-delete"
                    variant="outline"
                    sx={{width: "114px"}}
                    size="sm"
                    onClick={handleUndoDelete}
                    disabled={deletedRows.length === 0}
                >
                    Undo Delete
                </Button>
                <Button
                    variant="outline"
                    sx={{width: "114px"}}
                    size="sm"
                    onClick={handleUndoUpdate}
                    disabled={updatedRecordsOldValues?.length === 0}
                >
                    Undo Update
                </Button>
            </div>
            <BasTabulator
                table={table}
                setTable={setTable}
                setDetail={setDetail}
                cellMenu={cellMenu}
                getData={getData}
                updateRow={updateRow}
            />
        </div>
    )
}