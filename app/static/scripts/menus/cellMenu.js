import table from "../table.js";
import {multiColumnFilter} from "../filter.js";
import {state} from "../table.js";

const cellMenu = [
    {
        label: "<i class=\"fa-solid fa-filter\"></i> Filter By Cell Value",
        action: function (e, cell) {
            const value = cell.getValue()
            const valueEl = document.getElementById('filter-value')
            valueEl.value = value
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
            table.selectRow('visible')
        }
    },

    {
        label: "<i class=\"fa-solid fa-copy\"></i> Copy Selected Rows",
        action: function (e, cell) {
            table.copyToClipboard("selected"); //copy the currently selected rows to the clipboard
        }
    },

    {
        label: "<i class=\"fa-solid fa-minus\"></i> Deselect All Rows",
        action: function (e, cell) {
            table.deselectRow(table.getSelectedRows());
        }
    },
    {
        label: "<i class=\"fa-solid fa-download\"></i> Download Selected to xls",
        action: function (e, cell) {
            table.download("xlsx", "data.xlsx", {sheetName: "MyData"}, "selected");
        }
    },


    {
        separator: true,
    },
    {
        label: "Delete Functions",
        menu: [
            {
                label: "<i class=\"fa-solid fa-trash-arrow-up\"></i> Delete Row In Focus",
                action: function (e, cell) {
                    const row = cell.getRow()
                    const id = row.getData().id
                    row.delete();
                    state.deletedRows.push(id)

                }
            },
            {
                label: "<i class=\"fa-solid fa-trash-can\"></i> Delete Selected Rows",
                action: function (e, cell) {
                    const selectedRows = table.getSelectedRows();
                    const ids = []
                    selectedRows.forEach((r) => {
                        state.deletedRows.push(r.getData().id)
                        r.delete()
                    })
                }
            },
            // {
            //     label:"<i class='fas fa-ban'></i> Disabled Option",
            //     disabled:true,
            // },
        ]
    }
]


export default cellMenu