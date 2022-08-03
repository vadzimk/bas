import table from "../table.js";
import {multiColumnFilter} from "../filter.js";

const cellMenu = [
    {
        label: "<i class='fas fa-check-square'></i> Filter By Cell Value",
        action: function (e, cell) {
            const value = cell.getValue()
            const valueEl = document.getElementById('filter-value')
            valueEl.value = value
            multiColumnFilter(value, table)
            if(!value){
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
        label: "<i class='fas fa-check-square'></i> Toggle Select Row",
        action: function (e, cell) {
            const row = cell.getRow()
            row.toggleSelect();
        }
    },
    {
        label: "<i class='fas fa-check-square'></i> Select Visible Rows",
        action: function (e, cell) {
            table.selectRow('visible')
        }
    },

    {
        label: "<i class='fas fa-check-square'></i> Copy Selected Rows",
        action: function (e, cell) {
            table.copyToClipboard("selected"); //copy the currently selected rows to the clipboard
        }
    },

    {
        label: "<i class='fas fa-check-square'></i> Deselect All Rows",
        action: function (e, cell) {
            table.deselectRow(table.getSelectedRows());
        }
    },
    {
        label: "<i class='fas fa-check-square'></i> Download Selected to XLSX",
        action: function (e, cell) {
            table.download("xlsx", "data.xlsx", {sheetName: "MyData"}, "selected");
        }
    },


    {
        separator: true,
    },
    {
        label: "Admin Functions",
        menu: [
            {
                label: "<i class='fas fa-trash'></i> Delete Row In Focus",
                action: function (e, cell) {
                    const row = cell.getRow()
                    row.delete();
                }
            },
            {
                label: "<i class='fas fa-trash'></i> Delete Selected Rows",
                action: function (e, cell) {
                    const selectedRows = table.getSelectedRows();
                    selectedRows.forEach((r) => {
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