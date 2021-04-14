// Copyright (c) 2016, libracore AG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expiring Licenses"] = {
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
        }
	]
};
