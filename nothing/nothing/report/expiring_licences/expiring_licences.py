# Copyright (c) 2021, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = [
            {"label": _("Licence"), "fieldname": "licence", "fieldtype": "Link", "options": "Licences", "width":"150"},
            {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width":"200"},
            {"label": _("Customer Contact Person"), "fieldname": "cust_contact_person", "fieldtype": "Link", "options": "Contact", "width":"100"},
            {"label": _("Billing Invervall"), "fieldname": "billing_intervall", "fieldtype": "Select", "width":"200"},
            {"label": _("Responsible"), "fieldname": "responsible", "fieldtype": "Link", "options": "User", "width":"200"},
            {"label": _("Expiration Date"), "fieldname": "expiration_date", "fieldtype": "Date", "width":"200"}
            ]
            
    if filters:
        data = get_licences(responsible=filters.responsible, customer=filters.customer, 
                billing_intervall=filters.billing_intervall, from_date=filters.from_date, 
                to_date=filters.to_date)
    else:
        data = get_licences()
        
    return columns, data


def get_licences(responsible=None, customer=None, billing_intervall=None, from_date=None, to_date=None):
    
    if not customer: 
        customer = "%"
    additional_conditions = ""
    if responsible: 
        additional_conditions += """ AND `tabLicences`.`responsible` = '{0}' """.format(responsible)
    if billing_intervall:
        additional_conditions += """ AND `tabLicences`.`billing_intervall` = '{0}'""".format(billing_intervall)
    if from_date:
        additional_conditions += """ AND (`tabLicences`.`expiration_date` >= '{from_date}' OR `tabLicences`.`expiration_date` IS NULL)""".format(from_date=from_date)
    if to_date:
        additional_conditions += """ AND (`tabLicences`.`expiration_date` <= '{to_date}' OR `tabLicences`.`expiration_date` IS NULL)""".format(to_date=to_date)
        
    sql_query = """SELECT 
                `tabLicences`.`name` AS `licence`,
                `tabLicences`.`customer` AS `customer`,
                `tabLicences`.`cust_contact_person` AS `cust_contact_person`,
                `tabLicences`.`responsible` AS `responsible`,
                `tabLicences`.`billing_intervall` AS `billing_intervall`,
                `tabLicences`.`expiration_date` AS `expiration_date`
    FROM `tabLicences`
    WHERE `tabLicences`.`customer` LIKE  '{customer}' {additional_conditions}
    ORDER BY `tabLicences`.`expiration_date` ASC;
    """.format(customer=customer, additional_conditions=additional_conditions)
    
     
    data = frappe.db.sql(sql_query, as_dict = True)
    return data
