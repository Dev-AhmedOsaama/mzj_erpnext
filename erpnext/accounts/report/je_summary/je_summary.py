# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data



def get_data(filters):
	data1 = frappe.db.sql(f"""select 
						'total' as account,
						sum(credit) as credit,
						sum(debit) as debit,
						(sum(debit) - sum(credit)) as balance
						from 
							`tabJournal Entry Account`
						where
							parent = '{filters.get('journal_entry')}'""", as_dict=1)
	data = frappe.db.sql(f"""select
						account,
						credit,
						debit,
						(debit - credit) as balance,
						user_remark
						from 
							`tabJournal Entry Account`
						where
							parent = '{filters.get('journal_entry')}'
						order by idx asc""", as_dict=1)
	if data and data1:
		data.extend(data1)
		return data
	else:
		return []

def get_columns(filters):
	return [
		{
			"fieldname": "account",
			"label": "Account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 200
		},
		{
			"fieldname": "debit",
			"label": "Debit",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "credit",
			"label": "Credit",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "balance",
			"label": "Balance",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "user_remark",
			"label": "User Remark",
			"fieldtype": "Data",
			"width": 600
		}
	]