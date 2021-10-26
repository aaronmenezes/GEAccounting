# Copyright (c) 2013, aaron M and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _

def execute(filters=None):
	data = get_data()
	columns = get_column_list()
	return columns, data

def  get_column_list(): 
	columns =[
		{
			"fieldname" : "account",
			"label" : _("Account"),
			"fieldtype" : "Link",
			"options" : "StoreAccounts",
			"width" : 400
		},
		{
			"fieldname" : "amount",
			"label" : _("Amount"),
			"fieldtype" : "Currency",
			"width" : 400
		},
		{
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"width": 400
		}
		]
	return columns

def get_data():  
	data = []  
	total_liabilities = 0  
	summary = get_gl_amounts('credit_amount','Assets',root_type=['Asset','Expense'])
	data.extend(summary) 
	data.append({})
	summary = get_gl_amounts('debit_amount','Liabilities',root_type=['Income', 'Liability','Equity'])
	data.extend(summary)  
	return data

def get_gl_amounts(field_name,parent_account,root_type):
	total_amounts=0
	line_item=[{ 'indent': 0, 'account': parent_account}]
	root_type.insert(0,'=') 
	accounts = frappe.get_all( 'StoreAccounts',
		filters = { 'root_type': root_type},
		pluck = 'name'
	)
	for ledger_entry in frappe.get_all( 'StoreGL', group_by='account',
		filters={ 'account': ['in', accounts] },
		fields=[ 'account', 'sum(%s) as total_amount'%field_name,field_name ]
	):
		line_item.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.total_amount,
			'parent_account': parent_account
		}) 
		total_amounts += ledger_entry.total_amount 
	line_item.append({
		'intend': 0,
		'account': 'Total %s'%parent_account,
		'total': total_amounts
	})
	return line_item
