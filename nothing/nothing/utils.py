# -*- coding: utf-8 -*-
# Copyright (c) 2021, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import nowdate, add_days, add_months, add_years, getdate, add_to_date, get_datetime, get_datetime_str
from datetime import date, timedelta

@frappe.whitelist()
def create_task(project, task_type, description, item_name, expected_time='', exp_start_date='', exp_end_date='', completed_by=''):
    task = frappe.get_doc({
        "doctype": "Task",
        "project": project,
        "type": task_type,
        "description": description,
        "expected_time": expected_time,
        "exp_start_date": exp_start_date,
        "exp_end_date": exp_end_date,
        "completed_by": completed_by,
        "subject": item_name
    })
    task.insert()
    
    return task.name
    
@frappe.whitelist()
def create_tasks_from_so(so):
    so = frappe.get_doc("Sales Order", so)
    project = frappe.db.sql("""SELECT `name` FROM `tabProject` WHERE `sales_order` = '{so}'""".format(so=so.name), as_dict=True)[0].name

    for item in so.items:
        task = frappe.get_doc({
            "doctype": "Task",
            "project": project,
            "expected_time": item.qty,
            "subject": item.item_name
        })
        task.insert()
        
        item_master = frappe.get_doc("Item", item.item_code)
        item_master.task = task.name
        item_master.save()
        
    return

@frappe.whitelist()
def licence_invoice_run(licence=None):
    if licence:
        licences = [{'name': licence}]
    else:
        # no licence provided, select all due licences
        sql_query = """SELECT `name` 
                       FROM `tabLicences` 
                       WHERE `next_billing_date` <= '{date}' AND `disabled` != 1""".format(date=nowdate())
        licences = frappe.db.sql(sql_query, as_dict=True)
    
    sinvs = []
    for _licence in licences:
        try:
            # create invoice
            sinv = create_licence_invoice(_licence['name'])
            sinvs.append(sinv)
            
            # pull licence document to update
            licence_doc = frappe.get_doc("Licences", _licence['name'])
            # update expiration_date of licence
            if licence_doc.billing_intervall == 'monthly':
                licence_doc.next_billing_date = add_months(licence_doc.next_billing_date, 1)
                licence_doc.expiration_date = add_months(licence_doc.expiration_date, 1)
            else:
                licence_doc.next_billing_date = add_years(licence_doc.next_billing_date, 1)
                licence_doc.expiration_date = add_years(licence_doc.expiration_date, 1)
            licence_doc.save()
        except Exception as e:
            frappe.log_error(e, 'licence_invoice_run')
    return sinvs

@frappe.whitelist()
def create_licence_invoice(licence_name):
    # pull licence
    licence = frappe.get_doc("Licences", licence_name)
    # load settings
    settings = frappe.db.sql("""SELECT * 
                  FROM `tabNothing Settings Licence Details` 
                  WHERE `company` = "{company}";""".format(company=licence.company), as_dict=True)
    if settings and len(settings) > 0:
        settings = settings[0]
    else:
        frappe.throw("Configuration missing for licence invoices (see Nothing Settings)")
    taxes_and_charges = settings['taxes_ch'] if licence.default_currency == 'CHF' else settings['taxes_other']
    income_account = settings['income_account_ch'] if licence.default_currency == 'CHF' else settings['income_account_other']
    
    # collect invoice items from licence
    sinv_items = []
    for item in licence.items:
        this_item = {
                'item_code': item.item_code,
                'qty': item.qty,
                'uom': item.stock_uom,
                'rate': item.rate,
                'licences': licence.name,
                'description': item.description,
                'cost_center': settings['cost_center'],
                'income_account': income_account
            }
        sinv_items.append(this_item)
    
    # create invoice record
    sinv = frappe.get_doc({
        "doctype": "Sales Invoice",
        "naming_series": settings['naming_series'],
        "customer": licence.customer,
        'serviceperiod_from_date': add_months(licence.expiration_date, -1) if licence.billing_intervall == 'monthly' else add_years(licence.expiration_date, -1),
        'serviceperiod_to_date': licence.expiration_date,
        'responsible': licence.responsible,
        'contact_person': licence.cust_contact_person,
        'po_no': licence.cust_po_nr,
        'company': licence.company,
        'taxes_and_charges': taxes_and_charges,
        'additional_discount_percentage': licence.discount,
        'apply_discount_on': 'Net Total',
        "items": sinv_items
    })
    sinv.insert()
    return sinv.name
    
@frappe.whitelist()
def create_split_invoice(sales_order):
    items = []
    
    for item in sales_order.items:
        _item = {
            'item_code': sales_order.item_code,
            'qty': sales_order.qty,
            'uom': sales_order.stock_uom,
            'rate': sales_order.rate,
            'licences': sales_order.name,
            'description': sales_order.description,
            'cost_center': cost_center,
            'income_account': income_account
        }
        items.append(_item)
    
    sinv = frappe.get_doc({
        "doctype": "Sales Invoice",
        "naming_series": naming_series,
        "customer": sales_order.customer,
        'responsible': sales_order.responsible,
        'contact_person': sales_order.cust_contact_person,
        'company': sales_order.company,
        'product_title': sales_order.product_title,
        'taxes_and_charges': sales_order.taxes_and_charges,
        'additional_discount_percentage': sales_order.discount,
        'apply_discount_on': 'Net Total',
        "items": items
    })
    sinv.insert()
    return sinv.name

@frappe.whitelist()
def create_timesheet_entry(task, date, activity_type, hours, description=''):
    task = frappe.get_doc("Task", task)
    employee = frappe.db.sql("""SELECT `name` FROM `tabEmployee` WHERE `user_id` = '{user}' AND `status` = 'Active'""".format(user=frappe.session.user), as_dict=True)
    try:
        employee = employee[0].name
    except:
        frappe.throw(_("No employee found"))
    
    billing_rate = get_billing_rate(task.project, activity_type, employee)
    #return billing_rate
        
    existing_ts = frappe.db.sql("""SELECT `name`, `docstatus` FROM `tabTimesheet`
                                    WHERE `employee` = '{employee}'
                                    AND `start_date` = '{date}'
                                    AND `docstatus` != 2""".format(employee=employee, date=date), as_dict=True)
    # check if timesheet exists
    if len(existing_ts) > 0:
        if existing_ts[0].docstatus != 0:
            frappe.throw(_("Timesheet already submitted for this date, please cancel and amend"))
        # add to existing timesheet
        timesheet = frappe.get_doc("Timesheet", existing_ts[0].name)
        latest_entry = frappe.db.sql("""SELECT `to_time` FROM `tabTimesheet Detail` WHERE `parent` = '{parent}' ORDER BY `to_time` DESC""".format(parent=timesheet.name), as_dict=True)
        latest_datetime = latest_entry[0].to_time
        row = timesheet.append("time_logs", {})
        row.activity_type = activity_type
        row.from_time = latest_datetime
        row.to_time = get_datetime(add_to_date(latest_datetime, hours=float(hours)))
        row.hours = float(hours)
        row.task = task.name
        row.project = task.project
        row.billing_rate = billing_rate
        row.billable = 1
        row.billing_hours = float(hours)
        row.ts_description = description
        timesheet.save()
        return timesheet.name
    else:
        # create new timesheet
        timesheet = frappe.get_doc({
            "doctype": "Timesheet",
            "company": task.company,
            "employee": employee,
            "start_date": date,
            "end_date": date,
            "time_logs": [
                {
                    "activity_type": activity_type,
                    "from_time": date + " 06:00:00",
                    "to_time": get_datetime(add_to_date(date + " 06:00:00", hours=float(hours))),
                    "hours": float(hours),
                    'task': task.name,
                    'project': task.project,
                    'billable': 1,
                    'billing_hours': float(hours),
                    'ts_description': description,
                    'billing_rate': billing_rate
                }
            ],
        })
        timesheet.insert()
        return timesheet.name
        
@frappe.whitelist()
def get_billing_rate(project, activity_type, employee):
    project = frappe.get_doc("Project", project)
    billing_rate = project.project_billing_rate
    if len(project.flex_billing_rate) > 0:
        special_rate = False
        # case/prio 1 matching of activity_type and employee
        for flex_rate in project.flex_billing_rate:
            if flex_rate.activity_type == activity_type and flex_rate.employee == employee:
                special_rate = flex_rate.flex_billing_rate
                billing_rate = special_rate
                return billing_rate
        # case/prio 2 matching only employee w/o activity_type
        if not special_rate:
            for flex_rate in project.flex_billing_rate:
                if not flex_rate.activity_type and flex_rate.employee == employee:
                    special_rate = flex_rate.flex_billing_rate
                    billing_rate = special_rate
                    return billing_rate
        # case/prio 3 matching only activity_type w/o employee
        if not special_rate:
            for flex_rate in project.flex_billing_rate:
                if flex_rate.activity_type == activity_type and not flex_rate.employee:
                    special_rate = flex_rate.flex_billing_rate
                    billing_rate = special_rate
                    return billing_rate
    else:
        return billing_rate
    return billing_rate

@frappe.whitelist()
def get_item_rate(currency, item_code):
    rates = frappe.db.sql("""SELECT `price_list_rate` FROM `tabItem Price` WHERE
                            `currency` = '{currency}'
                            AND `item_code` = '{item_code}'
                            AND `selling` = 1
                            ORDER BY `modified` DESC LIMIT 1""".format(currency=currency, item_code=item_code), as_list=True)
    if len(rates) > 0:
        rate = rates[0][0]
        return rate
    else:
        return '0.00'

@frappe.whitelist()
def get_timelogs_of_task_items(sinv):
    data = {}
    sinv = frappe.get_doc("Sales Invoice", sinv)
    for _item in sinv.items:
        item = frappe.get_doc("Item", _item.item_code)
        uom = _item.uom
        data[item.item_code] = {
            'qty': 0,
            'rate': 0
        }
        
        time_logs = frappe.db.sql("""SELECT SUM(`billing_amount`) AS `billing_amount`, SUM(`hours`) AS `hours` FROM `tabTimesheet Detail`
                                        WHERE `task` = '{task}' AND `docstatus` != 2 AND `billable` = 1""".format(task=item.task), as_dict=True)
        
        if len(time_logs) > 0:
            #frappe.throw(str(time_logs))
            if time_logs[0].hours:
                if uom == "h":
                    data[item.item_code]["qty"] = time_logs[0].hours
                    data[item.item_code]["rate"] = time_logs[0].billing_amount / time_logs[0].hours
                else:
                    data[item.item_code]["qty"] = time_logs[0].hours / 8
                    data[item.item_code]["rate"] = time_logs[0].billing_amount / time_logs[0].hours * 8
    return data

def create_holiday_timesheet(doc, method):
    company = doc.company
    from_date = doc.from_date
    to_date = doc.to_date
    year = getdate(from_date).strftime("%Y")
    timelogs = []
    try:
        #activity_type = frappe.get_doc("Worktime Settings", "Worktime Settings").activity_type_determination[0].activity_type
        # take activity_type from leave_type
        activity_type = doc.leave_type
    except:
        activity_type = "Urlaub"
    if doc.half_day:
        if doc.half_day_date:
            half_day_date = doc.half_day_date
        else:
            half_day_date = doc.from_date
    else:
        half_day_date = False
    
    holiday_lists = frappe.db.sql("""SELECT `year`, `public_holiday_list` FROM `tabPublic Holiday List` WHERE `year` = '{year}' AND `company` = '{company}' LIMIT 1""".format(year=year, company=company), as_dict=True)
    if len(holiday_lists) > 0:
        holiday_list = holiday_lists[0].public_holiday_list
        _holiday_list_entries = frappe.db.sql("""SELECT `holiday_date` FROM `tabHoliday` WHERE `parent` = '{holiday_list}'""".format(holiday_list=holiday_list), as_list=True)
        holiday_list_entries = []
        
        for entry in _holiday_list_entries:
            holiday_list_entries.append(entry[0])
            
        start_date = getdate(from_date)
        end_date = getdate(to_date)
        delta = timedelta(days=1)
        
        while start_date <= end_date:
            if start_date not in holiday_list_entries:
                filters = frappe._dict()
                filters.company = doc.company
                filters.to_date = start_date
                filters.from_date = start_date
                hours = get_daily_hours(company)
                from_time = get_datetime(get_datetime_str(start_date.strftime("%Y-%m-%d") + " 08:00:00"))
                if half_day_date:
                    if start_date == half_day_date:
                        hours = hours / 2
                to_time = add_to_date(from_time, hours=hours)
                timelogs.append({
                    "activity_type": activity_type,
                    "hours": hours,
                    "from_time": from_time,
                    "to_time": to_time
                })
            start_date += delta
        
        ts = frappe.get_doc({
            "doctype": "Timesheet",
            "employee": doc.employee,
            "time_logs": timelogs
        })
        ts.insert(ignore_permissions=True)
        ts.submit()
        
def get_daily_hours(company):
    try:
        daily_hours = frappe.db.sql("""SELECT `daily_hours` FROM `tabDaily Hours` WHERE `company` = '{company}' LIMIT 1""".format(company=company), as_list=True)[0][0]
    except:
        # fallback
        daily_hours = 8
    return daily_hours
