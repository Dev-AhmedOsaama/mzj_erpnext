// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["JE summary"] = {
	"filters": [

		{
			"fieldname":"journal_entry",
			"label": __("Journal Entry"),
			"fieldtype": "Link",
			"options": "Journal Entry",
			"reqd": 1
		},
	]
};
