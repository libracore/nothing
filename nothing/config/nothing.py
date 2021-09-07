from __future__ import unicode_literals
from frappe import _


def get_data():
    return[
        {
            "label": _("Selling"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Customer",
                       "label": _("Customer"),
                       "description": _("Customer")
                   },
                   {
                       "type": "doctype",
                       "name": "Contact",
                       "label": _("Contact"),
                       "description": _("Contact")
                   },
                   {
                       "type": "doctype",
                       "name": "Quotation",
                       "label": _("Quotation"),
                       "description": _("Quotation")
                   },
                   {
                       "type": "doctype",
                       "name": "Sales Order",
                       "label": _("Sales Order"),
                       "description": _("Sales Order")
                   },
                   {
                       "type": "doctype",
                       "name": "Delivery Note",
                       "label": _("Delivery Note"),
                       "description": _("delivery Note")
                   },
                   {
                       "type": "doctype",
                       "name": "Sales Invoice",
                       "label": _("Sales Invoice"),
                       "description": _("Sales Invoice")
                   },
                   {
                       "type": "doctype",
                       "name": "Payment Entry",
                       "label": _("Payment Entry"),
                       "description": _("Payment Entry")
                   },
                   {
                       "type": "doctype",
                       "name": "Nothing Settings",
                       "label": _("Licence Settings"),
                       "description": _("Licence Settings")         
                   }
            ]
        },
        {
            "label": _("Projects & Co"),
            "icon": "octicon octicon-file-submodule",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Project",
                       "label": _("Project"),
                       "description": _("Project")
                   },
                   {
                       "type": "doctype",
                       "name": "Task",
                       "label": _("Task"),
                       "description": _("Task")
                   },
                   {
                       "type": "doctype",
                       "name": "Item",
                       "label": _("Item"),
                       "description": _("Item")
                   },
                   {
                       "type": "doctype",
                       "name": "Timesheet",
                       "label": _("Timesheet"),
                       "description": _("Timesheet")
                   }                                         
            ]
        },
        {
            "label": _("Purchasing"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Supplier",
                       "label": _("Supplier"),
                       "description": _("Supplier")
                   },
                   {
                       "type": "doctype",
                       "name": "Purchase Order",
                       "label": _("Purchase Order"),
                       "description": _("Purchase Order")
                   },
                   {
                       "type": "doctype",
                       "name": "Purchase Receipt",
                       "label": _("Purchase Receipt"),
                       "description": _("Purchase Receipt")
                   },
                   {
                       "type": "doctype",
                       "name": "Purchase Invoice",
                       "label": _("Purchase Invoice"),
                       "description": _("Purchase Invoice")
                   },
                   {
                       "type": "doctype",
                       "name": "Payment Entry",
                       "label": _("Payment Entry"),
                       "description": _("Payment Entry")
                   }
            ]
        },
        {
            "label": _("HR"),
            "icon": "octicon octicon-list-ordered",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Employee",
                       "label": _("Employee"),
                       "description": _("Employee")
                   },
                   {
                       "type": "doctype",
                       "name": "Leave Application",
                       "label": _("Leave Application"),
                       "description": _("Leave Application")
                   },                   
                   {
                       "type": "doctype",
                       "name": "Leave Allocation",
                       "label": _("Leave Allocation"),
                       "description": _("Leave Allocation")
                   },
                   {
                       "type": "doctype",
                       "name": "Worktime Settings",
                       "label": _("Worktime Settings"),
                       "description": _("Worktime Settings")
                   },
                   {
                       "type": "report",
                       "doctype": "Timesheet",
                       "name": "Worktime Overview",
                       "label": _("Worktime Overview"),
                       "description": _("Worktime Overview"),
                       "is_query_report": True
                   }
            ]
        },
        {
            "label": _("Accounting"),
            "icon": "octicon octicon-repo",
            "items": [
                   {
                       "type": "page",
                       "name": "bank_wizard",
                       "label": _("Bank Wizard"),
                       "description": _("Bank Wizard")
                   },
                   {
                       "type": "doctype",
                       "name": "Payment Proposal",
                       "label": _("Payment Proposal"),
                       "description": _("Payment Proposal")
                   },
                   {
                       "type": "doctype",
                       "name": "Payment Reminder",
                       "label": _("Payment Reminder"),
                       "description": _("Payment Reminder")
                   },
                   {
                       "type": "report",
                       "name": "General Ledger",
                       "doctype": "GL Entry",
                       "is_query_report": True,
                   }
            ]
        },
        {
            "label": _("Automatisations"),
            "icon": "octicon octicon-repo",
            "items": [
                   {
                       "type": "Doctype",
                       "name": "Notification",
                       "label": _("Notification"),
                       "description": _("Notification")
                   },
                   {
                       "type": "Doctype",
                       "name": "Auto Email Report",
                       "label": _("Auto Email Report"),
                       "description": _("Auto Email Report")
                   }
            ]
        }
    ]
