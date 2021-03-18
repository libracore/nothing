# -*- coding: utf-8 -*-
# Copyright (c) 2021, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.data import nowdate, add_days, add_months, add_years

@frappe.whitelist()
def create_task(project, task_type, description, item_name):
	task = frappe.get_doc({
		"doctype": "Task",
		"project": project,
		"type": task_type,
		"description": description,
		"subject": item_name
	})
	task.insert()
	
	return task.name

@frappe.whitelist()
def licence_invoice_run(single_run=False):
	#not single, loops through all valid licences
	if not single_run:
		sql_query = """SELECT `name` FROM `tabLicences` WHERE `next_billing_date` <= '{date}' AND `disabled` != 1""".format(date=nowdate())
		licences = frappe.db.sql(sql_query, as_list=True)
		
		for _licence in licences:
			licence = frappe.get_doc("Licences", _licence[0])
			if licence:
				try:
					# create invoice
					sinv = create_licences_invoice(licence)
					
					# update expiration_date of licence
					if licence.billing_intervall == 'monthly':
						licence.next_billing_date = add_months(licence.next_billing_date, 1)
						licence.expiration_date = add_months(licence.expiration_date, 1)
					else:
						licence.next_billing_date = add_years(licence.next_billing_date, 1)
						licence.expiration_date = add_years(licence.expiration_date, 1)
					licence.save()
				except Exception as e:
					frappe.log_error(e, 'licence_invoice_run')
		return
	#button on licence to create single one
	else:
		licence = frappe.get_doc("Licences", single_run)
		if licence:
			try:
				# create invoice
				sinv = create_licences_invoice(licence)
				
				# update expiration_date of licence
				if licence.billing_intervall == 'monthly':
					licence.next_billing_date = add_months(licence.next_billing_date, 1)
					licence.expiration_date = add_months(licence.expiration_date, 1)
				else:
					licence.next_billing_date = add_years(licence.next_billing_date, 1)
					licence.expiration_date = add_years(licence.expiration_date, 1)
				licence.save()
				return sinv
			except Exception as e:
				frappe.log_error(e, 'licence_invoice_run')
				return {
					'error': e
				}
				
def create_licences_invoice(licence):
	sinv = frappe.get_doc({
		"doctype": "Sales Invoice",
		"customer": licence.customer,
		'serviceperiod_from_date': add_months(licence.expiration_date, -1) if licence.billing_intervall == 'monthly' else add_years(licence.expiration_date, -1),
		'serviceperiod_to_date': licence.expiration_date,
		'responsible': licence.responsible,
		'contact_person': licence.cust_contact_person,
		"items": [
			{
				'item_code': licence.item,
				'qty': licence.peers,
				'licences': licence.name,
				'description': licence.description
			}
		]
	})
	sinv.insert()
	return sinv.name
