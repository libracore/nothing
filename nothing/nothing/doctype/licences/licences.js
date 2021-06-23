// Copyright (c) 2021, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Licences', {
	discount: function(frm) {
		update_discounted_net_total(frm);
	}
});

frappe.ui.form.on('Licences Invoice Items', {
	item_code: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];
		console.log(item)
		if ((item.item_code) && (frm.doc.default_currency)) {
			frappe.call({
				"method": "nothing.nothing.utils.get_item_rate",
				"args": {
					"currency": frm.doc.default_currency,
					"item_code": item.item_code
				},
				"callback": function(r) {
					if (r.message) {
						var rate = r.message;
						item.rate = rate;
						item.amount = item.qty * item.rate;
						cur_frm.refresh_field("items");
						update_net_total(frm);
						update_discounted_net_total(frm);
					}
				}
			});
		}
	},
	qty: function(frm, cdt, cdn) {
		update_amount(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn) {
		update_amount(frm, cdt, cdn);
		update_net_total(frm);
		update_discounted_net_total(frm);
	},
	amount: function(frm, cdt, cdn) {
		update_net_total(frm);
		update_discounted_net_total(frm);
	},
	items_remove: function(frm, cdt, cdn) {
		update_net_total(frm);
		update_discounted_net_total(frm);
	}
});

function update_amount(frm, cdt, cdn) {
	var item = locals[cdt][cdn];
	item.amount = item.qty * item.rate;
	cur_frm.refresh_field("items");
}

function update_net_total(frm) {
	var net_total = 0;
	for (var i = 0; i < frm.doc.items.length; i++) {
		net_total += frm.doc.items[i].amount;
	}
	cur_frm.set_value('net_total', net_total);
}

function update_discounted_net_total(frm) {
	var discounted_net = ((100 - frm.doc.discount) / 100) * frm.doc.net_total;
	cur_frm.set_value('discounted_net', discounted_net);
}
