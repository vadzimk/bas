
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


