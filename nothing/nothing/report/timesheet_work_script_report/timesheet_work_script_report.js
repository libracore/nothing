// Copyright (c) 2016, libracore AG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Timesheet Work Script Report"] = {
	"filters": [
        {
            "fieldname":"project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": "60px"
        },
        {
            "fieldname":"from_time",
            "label": __("Start"),
            "fieldtype": "Datetime",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "width": "60px"
         },
         {
            "fieldname":"to_time",
            "label": __("End"),
            "fieldtype": "Datetime",
            "default": frappe.datetime.get_today(),
            "width": "60px"
         }
    ]
};
