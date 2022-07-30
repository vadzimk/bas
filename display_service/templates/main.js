// -------------- Filter ------------------------
//Define variables for input elements
var fieldEl = document.getElementById("filter-field");
var typeEl = document.getElementById("filter-type");
var valueEl = document.getElementById("filter-value");

//Custom filter example
function customFilter(data) {
    return data.car && data.rating < 3;
}

//Trigger setFilter function with correct parameters
function updateFilter() {
    var filterVal = fieldEl.options[fieldEl.selectedIndex].value;
    var typeVal = typeEl.options[typeEl.selectedIndex].value;

    var filter = filterVal == "function" ? customFilter : filterVal;

    if (filterVal == "function") {
        typeEl.disabled = true;
        valueEl.disabled = true;
    } else {
        typeEl.disabled = false;
        valueEl.disabled = false;
    }

    if (filterVal) {
        table.setFilter(filter, typeVal, valueEl.value);
    }
}

//Update filters on value change
document.getElementById("filter-field").addEventListener("change", updateFilter);
document.getElementById("filter-type").addEventListener("change", updateFilter);
document.getElementById("filter-value").addEventListener("keyup", updateFilter);

//Clear filters on "Clear Filters" button click
document.getElementById("filter-clear").addEventListener("click", function () {
    fieldEl.value = "";
    typeEl.value = "=";
    valueEl.value = "";

    table.clearFilter();
});

// -------------------- Menus ----------------------
// ------------------- Row context menu -----------

//define row context menu contents
var rowMenu = [
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
            // {
            //     label:"<i class='fas fa-ban'></i> Disabled Option",
            //     disabled:true,
            // },
        ]
    }
]

// ---------------- Column Header menu ----------------

//define column header menu as column visibility toggle
var headerMenu = function () {
    var menu = [];
    var columns = this.getColumns();

    for (let column of columns) {

        //create checkbox element using font ! fantastic, fabulous, terrific, brilliant, marvellous, epic ! icons
        let icon = document.createElement("i");
        icon.classList.add("fas");
        icon.classList.add(column.isVisible() ? "fa-check-square" : "fa-square");

        //build label
        let label = document.createElement("span");
        let title = document.createElement("span");

        title.textContent = " " + column.getDefinition().title;

        label.appendChild(icon);
        label.appendChild(title);

        //create menu item
        menu.push({
            label: label,
            action: function (e) {
                //prevent menu closing
                e.stopPropagation();

                //toggle current column visibility
                column.toggle();

                //change menu item icon
                if (column.isVisible()) {
                    icon.classList.remove("fa-square");
                    icon.classList.add("fa-check-square");
                } else {
                    icon.classList.remove("fa-check-square");
                    icon.classList.add("fa-square");
                }
            }
        });
    }

    return menu;
};


// ----------------------- Download csv ------------------

//trigger download of data.csv file
document.getElementById("download-csv").addEventListener("click", function () {
    table.download("xlsx", "data.xlsx", {sheetName: "MyData"});
});

const newColumnNameInputElement = document.getElementById('new-column-name')

document.getElementById("add-column").addEventListener("click", function () {
    const columnName = newColumnNameInputElement.value
    if (columnName) {
        table.addColumn({title: columnName, field: columnName, editor: "input"}, false)
            .then((column) => {
                console.dir(column.getDefinition())
                newColumnNameInputElement.value = ''
            })
    }

});

document.getElementById("reset-table-layout").addEventListener("click", function () {
    window.localStorage.removeItem('tabulator-table-columns')
});

// ---------------------- Column Definitions ------------------------

function autoColumnsDefinitions(definitions) {
    //definitions - array of column definition objects

    definitions.forEach((column) => {
        column.headerFilter = true; // add header filter to every column
    });

    return definitions;
}

// ------------------------- Dragable panel ----------------------------

const BORDER_SIZE = 8;
const panel = document.getElementById("right_panel");

let m_pos;
function resize(e){
  const dx = m_pos - e.x;
  m_pos = e.x;
  panel.style.width = (parseInt(getComputedStyle(panel, '').width) + dx) + "px";
}

panel.addEventListener("mousedown", function(e){
  if (e.offsetX < BORDER_SIZE) {
    m_pos = e.x;
    document.addEventListener("mousemove", resize, false);
  }
}, false);

document.addEventListener("mouseup", function(){
    document.removeEventListener("mousemove", resize, false);
}, false);