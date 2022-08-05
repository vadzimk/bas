// this is not used in favor of the cellMenu, because cellMenu can access current cell value


import table from "../table.js";
import positionPopups from "../positionPopups.js";

// ------------------- Row context menu -----------

//define row context menu contents
const rowMenu = [
    // {
    //     label:"<i class='fas fa-user'></i> Change Name",
    //     action:function(e, row){
    //         row.update({name:"Steve Bobberson"});
    //     }
    // },


    {
        label: "<i class='fas fa-check-square'></i> Toggle Select Row",
        action: function (e, row) {
            row.toggleSelect();
        }
    },
    {
        label: "<i class='fas fa-check-square'></i> Select Visible Rows",
        action: function (e, row) {
            table.selectRow('visible')
        }
    },

    {
        label: "<i class='fas fa-check-square'></i> Copy Selected Rows",
        action: function (e, row) {
            table.copyToClipboard("selected"); //copy the currently selected rows to the clipboard
        }
    },

    {
        label: "<i class='fas fa-check-square'></i> Deselect All Rows",
        action: function (e, row) {
            table.deselectRow(table.getSelectedRows());
        }
    },
    {
        label: "<i class='fas fa-check-square'></i> Download Selected to XLSX",
        action: function (e, row) {
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
                action: function (e, row) {
                    row.delete();
                }
            },
            {
                label: "<i class='fas fa-trash'></i> Delete Selected Rows",
                action: function (e, row) {
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


export default rowMenu