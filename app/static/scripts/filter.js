import table from "./table.js";

//-------------- Multi-column filter -------------

const valueEl = document.getElementById("filter-value");

valueEl.addEventListener("keyup", function () {
    const filters = [];
    const search = valueEl.value;
    if(!search){
        table.clearFilter()
        return
    }

    const columns = table.getColumns();

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
