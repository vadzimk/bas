//   http://tabulator.info/docs/5.3/columns#definition

// import rowMenu from "./menus/rowMenu.js";
import headerMenu from "./menus/headerMenu.js"
import autoColumnsDefinitions from "./autoColumnDefinitions.js";
import makeToolTipFunction from "./tooltip.js";
import attachDetail from "./attachDetail.js";
import cellMenu from "./menus/cellMenu.js";

const table = new Tabulator("#table", {
    // debugEventsExternal:true, //console log external events
    // debugEventsInternal:true, //console log internal events
    // ajaxURL: '/api/jobs',
    index: "job_id", //set the index field
    maxHeight: "80vh",
    // maxHeight: "100%",
    autoColumns: true,  // automatically make columns structure by examining the first row of the table.
    autoColumnsDefinitions: autoColumnsDefinitions,
    resizableColumnFit: false,
    history: true,
    layout: "fitColumns",  //  the table will resize columns so that they fit inside the width of the container.
    movableColumns: true,
    persistence: true, //enable table persistence
    persistenceMode: "local", //store persistence information in local storage
    clipboard: true, //enable clipboard functionality
    responsiveLayout: "collapse", // collapse columns that no longer fit on the table into a list under the row
    selectable: true,  // enable row selection
    validationMode:"manual", // no vaildation is automatically performed on edit
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


// window.onbeforeunload = function () { // save column layout before page reloads
//     const columnLayout = table.getColumnLayout()
//     window.localStorage.setItem("tabulator-backup-column-layout", JSON.stringify(columnLayout))
// }


// export function restoreColumnLayout() {
//     const columnLayout = window.localStorage.getItem('tabulator-backup-column-layout')
//     table.setColumnLayout(JSON.parse(columnLayout));
// }


axios.get('/api/jobs').then((res) => {
    table.setData(res.data)
    // restoreColumnLayout()
}).catch((err) => console.log(err))

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
    const job_id = cell.getRow().getData().Job_id
    const oldValue = cell.getOldValue()
    const newValue = cell.getValue()
    if (
        ([null, ""].includes(oldValue) && [null, ""].includes(newValue))
        || oldValue?.toString().trim() === newValue?.toString().trim() ) {  // no change in cell value
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
    axios.put('/api/job', recordToSend)
        .then(res => {
            table.setData(res.data);
            // restoreColumnLayout()
        })
        .catch(e => console.log(e))

})


export const state = {
    deletedRows: [],  // array of arrays of int
}

export default table;
