# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from functools import total_ordering
import frappe
from frappe import _
from erpnext.accounts.report.financial_statements import get_period_list

def execute(filters=None):
	columns, data = [], []
	period_list = get_period_list(filters.fiscal_year, filters.fiscal_year, '', '','Fiscal Year', "Monthly")
	columns =get_columns(period_list)
	data = get_data(period_list)
	return columns, data



def get_data(period_list):
	all_data = []
	# get supplier list
	supplier_list = frappe.db.get_list('Supplier',filters={'disabled':0},fields=['name'])
	# get data for each supplier
	if len(supplier_list)>0:
		for supplier in supplier_list:
			row = {}
			total_payment_amount = 0
			total_paid_amount = 0
			total_outstanding = 0
			for period in period_list:
				data = frappe.db.sql(f"""select 
											COALESCE(sum(`tabPayment Schedule`.payment_amount),0) as '{period['key']+'_payment_amount'}', 
											COALESCE(sum(`tabPayment Schedule`.paid_amount),0) as '{period['key']+'_paid_amount'}', 
											COALESCE(sum(`tabPayment Schedule`.outstanding),0) as '{period['key']+'_outstanding'}' 
										from 
											`tabPurchase Invoice` 
										inner join 
											`tabPayment Schedule` 
										on  
											`tabPayment Schedule`.parent = `tabPurchase Invoice`.name
										and 
											`tabPayment Schedule`.parenttype = "Purchase Invoice"
										and
											`tabPayment Schedule`.due_date between '{period['from_date']}' and '{period['to_date']}'
										and
											`tabPurchase Invoice`.docstatus = 1
										and
											`tabPurchase Invoice`.supplier = '{supplier['name']}'
										""",as_dict=1)
				if len(data)>0:
					row.update(data[0])
					total_payment_amount+=data[0][period['key']+'_payment_amount']
					total_paid_amount+=data[0][period['key']+'_paid_amount']
					total_outstanding+=data[0][period['key']+'_outstanding']
				else:
					row.update({period['key']+'_payment_amount':0,period['key']+'_paid_amount':0,period['key']+'_outstanding':0})
			row.update({'total_payment_amount':total_payment_amount,'total_paid_amount':total_paid_amount,'total_outstanding':total_outstanding})
			row.update({'supplier':supplier['name']})
			all_data.append(row)
		return all_data



def get_columns(period_list):
	columns = [{
		"fieldname": "supplier",
		"label": _("Supplier"),
		"fieldtype": "Link",
		"options": "Supplier",
		"width": 300
		}]

	for period in period_list:
		columns.append({
			"fieldname": period.key+'_payment_amount',
			"label": 'Amount '+period.label,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 200,
			'default': 0.0
		})
		columns.append({
			"fieldname": period.key+'_paid_amount',
			"label": 'Paid '+period.label,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 200
		})
		columns.append({
			"fieldname": period.key+'_outstanding',
			"label": 'Outstanding '+period.label,
			"fieldtype": "Currency",
			"options": "currency",
			"width": 200
		})
	columns.append({
		"fieldname": "total_payment_amount",
		"label": _("Total Payment Amount"),
		"fieldtype": "Currency",
		"options": "currency",
		"width": 200,
		'default': 0.0
	})
	columns.append({
		"fieldname": "total_paid_amount",
		"label": _("Total Paid Amount"),
		"fieldtype": "Currency",
		"options": "currency",
		"width": 200,
		'default': 0.0
	})
	columns.append({
		"fieldname": "total_outstanding",
		"label": _("Total Outstanding"),
		"fieldtype": "Currency",
		"options": "currency",
		"width": 200,
		'default': 0.0
	})
	return columns