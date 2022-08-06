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
            || column.field === 'name'
            || column.field.includes('overview')) {
            const url_fields = {
                'title': 'url',
                'name': 'homepage_url',
                'overview': 'profile_url',
            }
            // column.formatter = 'link';
            column.formatter = (cell, formatterParams, onRendered) => {
                const url = cell.getRow().getData()[`${url_fields[column.field]}`]
                if (url){
                    return `<a href="${url}">${cell.getValue()}</a>`
                } else {
                    return cell.getValue()
                }

            }
            // column.formatterParams = {
            //     label: (cell) => cell.getValue(),
            //     target: '_blank',
            //     url: (cell) => cell.getRow().getData()[`${url_fields[column.field]}`]
            // }
            column.editable = false

        }

        if (column.field === 'other_locations_employees') {
            column.tooltip = makeToolTipFunction(
                {
                    innerHtmlGetterFunction: (cell) =>
                        cell.getRow().getData().other_locations_employees_html
                })
        }

        if (column.field === 'date_posted') {
            column.title = 'Listing Age'
            column.formatter = function (cell, formatterParams, onRendered) {
                return Math.floor((new Date() - new Date(cell.getValue())) / 1000 / 60 / 60 / 24)
            }
        }

        // console.dir(column)

    });

    return definitions;
}
