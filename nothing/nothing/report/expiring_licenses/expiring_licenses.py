# Copyright (c) 2013, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
    columns, data = [], []
    columns = ["Licence:Link/Licences:150",
                "Customer::200",  
                "Customer Contact Person::200",     
                "Billing Intervall::100",           
                "Expiration Date::200"
               ]
               
    if filters:
        data = get_licenses(responsible=filters.responsible, customer=filters.customer, billing_intervall=filters.billing_intervall, as_list=True)
    else:
        data = get_licenses(as_list=True)
        
    return columns, data


# use as_list=True in case of later Export to Excel
def get_licenses(responsible=None, customer=None, billing_intervall=None, as_list=True):
    sql_query = """SELECT 
                `t1`.`naming_series` AS License,
                `t1`.`customer` AS Customer,
                `t1`.`responsible` AS Responsible,
                `t1`.`billing_intervall` AS Billing_Intervall,
                `t1`.`expiration_date` AS Expiration_Date
    FROM `tabLicences` AS `t1`"""
    if responsible:
        sql_query += """ WHERE `t1`.`responsible` = '{0}'""".format(responsible)
    elif customer:
        sql_query += """ WHERE `t1`.`customer` = '{0}'""".format(customer)
    elif billing_intervall:
        sql_query += """ WHERE `t1`.`billing_intervall` = '{0}'""".format(billing_intervall)
    sql_query += """ORDER BY `t1`.`expiration_date` ASC"""
    if as_list:
        data = frappe.db.sql(sql_query, as_list = True)
    else:
        data = frappe.db.sql(sql_query, as_dict = True)
    return data
