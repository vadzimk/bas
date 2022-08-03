//   http://tabulator.info/docs/5.3/columns#definition

import rowMenu from "./menus/rowMenu.js";
import headerMenu from "./menus/headerMenu.js"
import autoColumnsDefinitions from "./autoColumnDefinitions.js";
import makeToolTipFunction from "./tooltip.js";
import attachDetail from "./attachDetail.js";

const table = new Tabulator("#table", {
    height: "100%",
    data: table_data,
    autoColumns: true,  // automatically make columns structure by examining the first row of the table.
    autoColumnsDefinitions: autoColumnsDefinitions,
    resizableColumnFit: false,
    history: true,
    layout: "fitColumns",  //  the table will resize columns so that they fit inside the width of the container.
    rowContextMenu: rowMenu,
    movableColumns: true,
    columnDefaults: {
        tooltip: makeToolTipFunction(),
        editor: "input",
        headerMenu: headerMenu,
        resizable: 'header',
        headerTooltip: true,
        download: true,  // include hidden columns in the download

    },
    // persistence: true, //enable table persistence
    // persistenceMode: "local", //store persistence information in local storage
    clipboard: true, //enable clipboard functionality
    responsiveLayout: "collapse", // collapse columns that no longer fit on the table into a list under the row

})

    table.on('rowClick', function (e, row) {
        attachDetail(row)
    })

    table.on("cellEditing", function (cell) {
        attachDetail(cell.getRow())
    });

export default table;
