// http://tabulator.info/docs/5.3/columns#definition
// ---------------------- Column Definitions ------------------------

import makeToolTipFunction from "./tooltip.js";

export const set_flag_icon = '<i class=\'fa fa-check flag\'></i>'
export const unset_flag_icon = '<i class=""></i>'

export default function autoColumnsDefinitions(definitions) {
    //definitions - array of column definition objects

    definitions.forEach((column) => {
        // column.headerFilter = true; // add header filter to every column

        // Total calculations
        if (column.field === 'Job_title'
            || column.field.includes('flag')
            || column.field.includes('note')
        ) { // show row count
            column.bottomCalc = "count"
        }

        if (column.field.includes('description')
            || column.field.includes('url')
            || column.field.includes('id')
            || column.field.includes('html')
            || column.field === 'Job_estimated_salary'
            || column.field === 'Job_hiring_insights'
            || column.field.includes('salary')
            || column.field.includes('benefits')
            || column.field.includes('rating')

        ) {
            column.visible = false
        }

        column.editable = false
        if (column.field.includes('note')
            || column.field.includes('salary')
            || column.field.includes('benefits')
            || column.field.includes('rating')
            || column.field.includes('industry')
        ) {
            column.editable = true;
        }


        // +++++++++ Format as link +++++++++++
        if (column.field.includes('title')
            || column.field === 'Company_name'
            || column.field.includes('overview')) {
            const url_fields = {
                'Job_title': 'Job_url',
                'Company_name': 'Company_homepage_url',
                'Company_overview': 'Company_profile_url',
            }
            // column.formatter = 'link';
            column.formatter = (cell, formatterParams, onRendered) => {
                // TODO these urls are getting in the way when clicking uncommented for now
                const url = cell.getRow().getData()[`${url_fields[column.field]}`]
                if (url) {
                    return `<a href="${url}" target="_blank" style="color: blueviolet;">${cell.getValue()}</a>`
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

        // TODO throws error
        if (column.field === 'Company_other_locations_employees') {
            column.tooltip = makeToolTipFunction(
                {
                    innerHtmlGetterFunction: (cell) =>
                        cell.getRow().getData().Company_other_locations_employees_html
                })
        }

        if (column.field === 'Job_date_posted') {
            column.title = 'Posted Days Ago'
            column.formatter = function (cell, formatterParams, onRendered) {
                return Math.floor((new Date() - new Date(cell.getValue())) / 1000 / 60 / 60 / 24)
            }
            column.sorter = "number"
            column.editable = false;
            column.tooltip = false;
        }
        if (column.field.includes('flag')) {
            column.editable = false;
            column.width = '2em'
            column.formatter = (cell, formatterParams, onRendered) => {
                const value = cell.getValue()
                let inner;
                if (value) {
                    inner = set_flag_icon
                } else {
                    inner = unset_flag_icon
                }

                return `<button style="height: 20px; width: 20px;">${inner}</button>`
                // return inner
            }

            function flipValue(cell) {
                cell.setValue(!cell.getValue())
            }

            if (column.field === 'JobUserNote_plan_apply_flag') {
                column.cellClick = function (e, cell) {
                    //e - the click event object
                    //cell - cell component
                    flipValue(cell)
                    cell.getRow().getCell('JobUserNote_did_apply_flag').setValue(false)


                }
            } else if (column.field === 'JobUserNote_did_apply_flag') {
                column.cellClick = function (e, cell) {
                    //e - the click event object
                    //cell - cell component
                    flipValue(cell)
                    cell.getRow().getCell('JobUserNote_plan_apply_flag').setValue(false)
                }
                column.visible = true
            }
        }
        if (column.field.includes('number')) {
            column.sorter = "number"
            column.sorterParams = {
                thousandSeparator: ",",
                decimalSeparator: ".",
                alignEmptyValues: "top",
            }


        }

        // console.dir(column)

    });


    return definitions;
}
