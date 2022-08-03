// http://tabulator.info/docs/5.3/columns#definition
// ---------------------- Column Definitions ------------------------

import makeToolTipFunction from "./tooltip.js";

export default function autoColumnsDefinitions(definitions) {
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
