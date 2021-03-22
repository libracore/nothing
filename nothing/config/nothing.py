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
                   }
            ]
		}
	]
