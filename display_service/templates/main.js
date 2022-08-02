//-------------- Multi-column filter -------------
const valueEl = document.getElementById("filter-value");
valueEl.addEventListener("keyup", function () {
    const filters = [];
    const columns = table.getColumns();
    const search = valueEl.value;

    columns.forEach(function (column) {
        filters.push({
            field: column.getField(),
            type: "like",
            value: search,
        });
    });

    table.setFilter([filters]);
})

//Clear filter on "Clear Filters" button click
document.getElementById("filter-clear").addEventListener("click", function () {
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
    window.localStorage.removeItem('tabulator-table-columns')
});



// http://tabulator.info/docs/5.3/columns#definition
// ---------------------- Column Definitions ------------------------

function autoColumnsDefinitions(definitions) {
    //definitions - array of column definition objects

    definitions.forEach((column) => {
        // column.headerFilter = true; // add header filter to every column

        if (column.field.includes('description')
            || column.field.includes('url')
            || column.field.includes('id')
            || column.field.includes('html')
        ) {
            column.visible = false
        }

        // +++++++++ Format as linnk +++++++++++
        if (column.field.includes('title')
            || column.field.includes('company_name')
            || column.field.includes('company_overview')) {
            const url_fields = {
                'title': 'url',
                'company_name': 'company_homepage_url',
                'company_overview': 'company_profile_url',
            }
            column.formatter = 'link';
            column.formatterParams = {
                label: (cell) => cell.getValue(),
                target: '_blank',
                url: (cell) => cell.getRow().getData()[`${url_fields[column.field]}`]
            }
            column.editable = false

        }

        if (column.field === 'company_other_locations_employees') {
            console.log('hello from field definition')
            column.tooltip = makeToolTipFunction(
                {
                    innerHtmlGetterFunction: (cell) =>
                        cell.getRow().getData().company_other_locations_employees_html
                })
        }

        // console.dir(column)

    });

    return definitions;
}

// ------------------------- Draggable panel ----------------------------

const BORDER_SIZE = 8;
const panel = document.getElementById("right_panel");

let m_pos;

function resize(e) {
    const dx = m_pos - e.x;
    m_pos = e.x;
    panel.style.width = (parseInt(getComputedStyle(panel, '').width) + dx) + "px";
}

panel.addEventListener("mousedown", function (e) {
    if (e.offsetX < BORDER_SIZE) {
        m_pos = e.x;
        document.addEventListener("mousemove", resize, false);
    }
}, false);

document.addEventListener("mouseup", function () {
    document.removeEventListener("mousemove", resize, false);
}, false);


// ----------------------- ToolTip ----------------

function makeToolTipFunction({
                                 innerTextGetterFunction = (cell) => cell.getValue(),
                                 innerHtmlGetterFunction
                             } = {}) {
    return function tooltipFunction(e, cell, onRendered) {
        //e - mouseover event
        //cell - cell component
        //onRendered - onRendered callback registration function

        var el = document.createElement("div");
        el.style.maxWidth = "500px";
        el.style.font = "14px/1.3 Roboto";
        el.style.borderRadius = "4px";
        el.style.opacity = "0";
        el.style.transition = 'opacity .15s ease'
        const mouse_position_y = e.clientY
        const mouse_position_x = e.clientX
        const scroll_position_y = window.scrollY


        if (typeof innerHtmlGetterFunction === 'function') {
            el.innerHTML = innerHtmlGetterFunction(cell)
        } else
            el.innerText = innerTextGetterFunction(cell);

        onRendered(() => {
            const {y: oldY, height: height} = el.getBoundingClientRect()
            if (mouse_position_y - height < 0) {
                // element above the window
                let newY = height + mouse_position_y + scroll_position_y + 16;
                el.style.top = `${newY}px`;
                el.style.left = `${mouse_position_x + 16}px`
            }
            el.style.position = 'absolute';
            el.style.opacity = "1";
        })


        return el;
    }
}

