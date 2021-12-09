
# Copyright (c) 2021, libracore AG and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    data = []
    columns = [
            {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width":"100"},
            {"label": _("Employee Link"), "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width":"100"},
            {"label": _("Employee"), "fieldname": "employee_name", "fieldtype": "Data", "width":"100"},
            {"label": _("Activity Type"), "fieldname": "activity_type", "fieldtype": "Link", "options": "Activity Type", "width":"100"},
            {"label": _("Task Link"), "fieldname": "task", "fieldtype": "Link", "options": "Task", "width":"100"},
            {"label": _("Task Name"), "fieldname": "subject", "fieldtype": "Data", "width":"100"},
            {"label": _("Task Description"), "fieldname": "ts_description", "fieldtype": "Text", "width":"100"},
            {"label": _("From Time"), "fieldname": "from_time", "fieldtype": "Datetime", "width":"140"},
            {"label": _("Timesheet"), "fieldname": "name", "fieldtype": "Link", "options": "Timesheet", "width":"100"},
            {"label": _("Verrechenbare Stunden"), "fieldname": "billing_hours", "fieldtype": "Float", "width":"70"},
            {"label": _("Stunden"), "fieldname": "hours", "fieldtype": "Float", "width":"70"}
            ]
            
    if filters:
        data = get_data(project=filters.project, start_date=filters.start_date, end_date=filters.end_date)
    else:
        data = get_data()
        
    return columns, data


def get_data(project=None, start_date=None, end_date=None):
    if not project: 
        project = "IS NOT NULL"
    else:
        project = "= '{project}'".format(project=project)
    additional_conditions = ""
    if start_date:
        additional_conditions += """ AND (`tabTimesheet`.`start_date` >= '{start_date}' OR `tabTimesheet`.`start_date` IS NULL)""".format(start_date=start_date)
    if end_date:
        additional_conditions += """ AND (`tabTimesheet`.`end_date` <= '{end_date}' OR `tabTimesheet`.`end_date` IS NULL)""".format(end_date=end_date)
        
    sql_query = """SELECT 
                `tabTimesheet Detail`.`project` AS `project`,
                `tabTimesheet`.`employee` AS `employee`,                
                `tabTimesheet`.`employee_name` AS `employee_name`,
                `tabTimesheet Detail`.`activity_type` AS `activity_type`,
                `tabTimesheet Detail`.`hours` AS `hours`,
                `tabTimesheet Detail`.`billing_hours` AS `billing_hours`,
                `tabTimesheet Detail`.`task` AS `task`,
                `tabTask`.`subject` AS `subject`,
                `tabTimesheet Detail`.`ts_description` AS `ts_description`,
                `tabTimesheet Detail`.`from_time` AS `from_time`,
                `tabTimesheet Detail`.`to_time` AS `to_time`,
                `tabTimesheet`.`name` AS `name`,
                `tabTimesheet`.`start_date` AS `start_date`,
                `tabTimesheet`.`end_date` AS `end_date`
    FROM `tabTimesheet Detail`
    LEFT JOIN `tabTimesheet` ON `tabTimesheet Detail`.`parent` = `tabTimesheet`.`name`
    LEFT JOIN `tabTask` ON `tabTimesheet Detail`.`task` = `tabTask`.`name`
    WHERE `tabTimesheet Detail`.`project` {project} AND `tabTimesheet`.`docstatus` < 2{additional_conditions}
    ORDER BY `tabTimesheet Detail`.`project`, `tabTimesheet Detail`.`from_time` ASC
    """.format(project=project, additional_conditions=additional_conditions)
    
    data = frappe.db.sql(sql_query, as_dict = True)

    return data
