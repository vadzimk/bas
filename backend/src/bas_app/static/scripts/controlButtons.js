import table from "./table.js";
import {state} from "./table.js";


// ----------------------- Download xls ------------------

//trigger download of data.csv file
document.getElementById("download-xls").addEventListener("click", function () {
    table.download("xlsx", "data.xlsx", {sheetName: "MyData"});
});

// -------------- Upload CSV -------------------
//trigger AJAX load on "Load Data via AJAX" button click
document.getElementById("upload-csv").addEventListener("click", function () {
    table.import("csv", ".csv");
});

// ------------------- Add new column --------------------------

const newColumnNameInputElement = document.getElementById('new-column-name')

document.getElementById("add-column").addEventListener("click", function () {
    const columnName = newColumnNameInputElement.value
    if (columnName) {
        const newColumnDefinition = {
            title: columnName,
            field: columnName,
            editor: "input",
            shiftEnterSubmit: true, //submit cell value on shift enter
        }
        table.addColumn(newColumnDefinition, false)
            .then((column) => {
                console.dir(column.getDefinition())
                newColumnNameInputElement.value = ''
            })
    }

});

document.getElementById("reset-table-layout").addEventListener("click", function () {
    Object.keys(localStorage).forEach((key) => {
        if (key.startsWith('tabulator')) {
            window.localStorage.removeItem(key)
        }
    })
});

const undoDeleteButton = document.getElementById('undo-delete')
undoDeleteButton.addEventListener('click', function () {
    if (!state.deletedRows.length) {
        return
    }
    const {deletedRows} = state
    const idsToUnDelete = deletedRows[deletedRows.length - 1]
    unDeleteRows(idsToUnDelete)
    state.deletedRows.pop()
})

function unDeleteRows(jobIds) {
    if(!jobIds){
        console.log("jobIds", jobIds)
        return
    }
    const records = jobIds.map(id=>({job_id: id, job_is_deleted: false}))
    console.log("records to undo", records)
    axios.put('/api/jobs',  records)
        .then((res) => {
            table.setData(res.data)
            if(!state.deletedRows.length){
            undoDeleteButton.classList.remove('is-info')

            }
        }).catch((e) => {
        console.log(e)
    })
}
