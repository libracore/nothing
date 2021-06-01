/*Copyright (c) 2021, libracore AG and contributors
For license information, please see license.txt*/

frappe.ui.form.on('Licences Invoice Items', {
	item_code: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];
		console.log(item)
		if (item.item_code) {
			frappe.call({
				"method": "nothing.nothing.utils.get_item_rate",
				"args": {
					"licence": item.parent,
					"item_code": item.item_code
				},
				"callback": function(r) {
					if (r.message) {
						var rate = r.message;
						item.rate = rate;
						item.amount = item.qty * item.rate;
						cur_frm.refresh_field("items");
					}
				}
			});
		}
	},
	qty: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];
		item.amount = item.qty * item.rate;
		cur_frm.refresh_field("items");
	},
	rate: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];
		item.amount = item.qty * item.rate;
		cur_frm.refresh_field("items");
	}
});
