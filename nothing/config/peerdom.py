from __future__ import unicode_literals
from frappe import _


def get_data():
    return[
        {
            "label": _("Licences"),
            "icon": "octicon octicon-organization",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Licences",
                       "label": _("Licences"),
                       "color": "#f88c00",
                       "icon": "octicon octicon-person",
                       "description": _("Licences")                 
                   },
                   {
                       "type": "report",
                       "name": "Expiring Licences",
                       "doctype": "Licences",
                       "label": _("Expiring Licences"),
                       "is_query_report": True            
                   },
                   {
                       "type": "doctype",
                       "name": "Nothing Settings",
                       "label": _("Licence Settings"),
                       "description": _("Licence Settings")         
                   }
            ]
        }
    ]
