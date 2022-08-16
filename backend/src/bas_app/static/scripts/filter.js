import table from "./table.js";

//-------------- Multi-column filter -------------
export function multiColumnFilter(value, table) {
    const filters = [];
    if (!value) {
        table.clearFilter()
        return
    }
    const columns = table.getColumns();

    columns
        .filter(c => !c.getField().includes('url'))
        .forEach(function (column) {
            filters.push({
                field: column.getField(),
                type: "like",
                value: value,
            });
        });

    table.setFilter([filters]);
}

const valueEl = document.getElementById("filter-value");

valueEl.addEventListener("keyup", function () {
    const value = valueEl.value;
    multiColumnFilter(value, table)
})

//Clear filter on "Clear Filters" button click
document.getElementById("filter-clear").addEventListener("click", function () {
    valueEl.value = "";
    table.clearFilter();
});
