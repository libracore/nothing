# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "nothing",
			"color": "orange",
			"icon": "fa fa-codepen",
			"type": "module",
			"label": _("Nothing")
		},
		{
			"module_name": "peerdom",
			"color": "green",
			"icon": "fa fa-dice-d20",
			"type": "module",
			"label": _("Peerdom")
		}
	]
