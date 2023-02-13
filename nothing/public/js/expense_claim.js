frappe.ui.form.on('Expense Claim', {
	refresh(frm) {
		// your code here
		var current_user = frappe.session.user;
		frappe.call({
            'method': "frappe.client.get_list",
            'args':{
         	    'doctype': "Employee",
             	'filters': [
             	    ["user_id","IN", [current_user]]
             	],
            },
            'callback': function (response) {
                var employee = response.message[0];
                if (employee) {
                    frm.set_value("employee", employee.name);
                    frm.add_custom_button(__("Select Approver"), function() {
                        get_approver(frm, employee.name);
                    });
                }
            }
        });
        
        
	}
});

function get_approver(frm, current_user) {
    
    frappe.call({
        'method': "frappe.client.get_list",
        'args':{
     	    'doctype': "Organisational Unit",
         	'filters': [
             	    ["employee","IN", [current_user]]
            ],
            fields: ["name","expense_approver"]
        },
        'callback': function (response) {
            var user_org_unit = response.message;
            var options = response.message.map(function(depa) {
                return { value: depa.name };
            });
            
            frappe.prompt([
                    {'fieldname': 'org_unit', 'fieldtype': 'Select', 'label': 'Organisational Unit', 'reqd': 1, 'options': options}  
               ],
               function(values){
                    for (var i = 0; i < user_org_unit.length; i++){
                        if (user_org_unit[i].name == values.org_unit) {
                            cur_frm.set_value("expense_approver", user_org_unit[i].expense_approver);
                        }
                    }
               },
               'Select Approver Department'
            );
        }
    });

}
