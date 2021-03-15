# -*- coding: utf-8 -*-
# Copyright (c) 2021, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

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
