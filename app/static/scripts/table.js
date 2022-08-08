//   http://tabulator.info/docs/5.3/columns#definition

// import rowMenu from "./menus/rowMenu.js";
import headerMenu from "./menus/headerMenu.js"
import autoColumnsDefinitions from "./autoColumnDefinitions.js";
import makeToolTipFunction from "./tooltip.js";
import attachDetail from "./attachDetail.js";
import cellMenu from "./menus/cellMenu.js";

const table = new Tabulator("#table", {
    maxHeight: "80vh",
    // maxHeight: "100%",
    // data: table_data,
    autoColumns: true,  // automatically make columns structure by examining the first row of the table.
    autoColumnsDefinitions: autoColumnsDefinitions,
    resizableColumnFit: false,
    history: true,
    layout: "fitColumns",  //  the table will resize columns so that they fit inside the width of the container.
    // rowContextMenu: rowMenu,
    movableColumns: true,
    selectable: true,
    persistence: true, //enable table persistence
    persistenceMode: "local", //store persistence information in local storage
    clipboard: true, //enable clipboard functionality
    responsiveLayout: "collapse", // collapse columns that no longer fit on the table into a list under the row
    columnDefaults: {
        tooltip: makeToolTipFunction(),
        editor: "input",
        headerMenu: headerMenu,
        resizable: 'header',
        headerTooltip: true,
        download: true,  // include hidden columns in the download
        contextMenu: cellMenu,

    },
})

axios.get('/jobs').then((res) => {
    table.setData(res.data)
}).catch((err) => console.log(err))

let currentRowElement;

function highlightCurrentRowElement(row) {
    if (currentRowElement) {
        currentRowElement.classList.remove('current-row')
    }
    currentRowElement = row.getElement()
    currentRowElement.classList.add('current-row')
}

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
    const column = cell.getField()
    const recordToSend = {
        id: cell.getRow().getData().id,
        [column]: cell.getValue()
    }
    axios.put('/job', recordToSend).catch(e => console.log(e))

})


export const state = {
    deletedRows: [],

}

export default table;
