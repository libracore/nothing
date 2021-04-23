// Copyright (c) 2016, libracore AG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expiring Licences"] = {
    "filters": [
        {
            "fieldname":"responsible",
            "label": __("Responsible"),
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname":"billing_intervall",
            "label": __("Billing Intervall"),
            "fieldtype": "Select",
            "options": ["monthly","yearly"]
        },
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -7),
            "width": "60px"
         },
         {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), +7),
            "width": "60px"
         }
    ]
};
