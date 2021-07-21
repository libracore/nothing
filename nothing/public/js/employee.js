frappe.ui.form.on('Employee', {
	from_date(frm) {
		if (cur_frm.doc.from_date && cur_frm.doc.to_date) {
            fetch_worktime_overview_html(frm);
        } else {
            cur_frm.set_df_property('worktime_overview_html','options','<div>Bitte Datum auswählen</div<');
        }
	},
    to_date(frm) {
		if (cur_frm.doc.from_date && cur_frm.doc.to_date) {
            fetch_worktime_overview_html(frm);
        } else {
            cur_frm.set_df_property('worktime_overview_html','options','<div>Bitte Datum auswählen</div<');
        }
	}
})

function fetch_worktime_overview_html(frm) {
    frappe.call({
        "method": "erpnextswiss.erpnextswiss.report.worktime_overview.worktime_overview.get_employee_overview_html",
        "args": {
            "employee": cur_frm.doc.name,
            "company": cur_frm.doc.company,
            "from_date": cur_frm.doc.from_date,
            "to_date": cur_frm.doc.to_date
        },
        "async": false,
        "callback": function(response) {
            var html = response.message;
            cur_frm.set_df_property('worktime_overview_html','options', html);
        }
    });
}
