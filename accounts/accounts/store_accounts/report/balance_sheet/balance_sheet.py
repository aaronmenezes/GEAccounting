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
	total_assets = 0
	total_liabilities = 0
	asset_accounts = frappe.get_all( 'StoreAccounts',
		filters = { 'root_type': ['=', 'Asset','Expense'] },
		pluck = 'name'
	)

	data.append({ 'indent': 0, 'account': 'Assets' })

	for ledger_entry in frappe.get_all( 'StoreGL', group_by='account',
		filters={ 'account': ['in', asset_accounts] },
		fields=[ 'account', 'credit_amount' ]
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.credit_amount,
			'parent_account': 'Assets'
		})
		total_assets += ledger_entry.credit_amount 
	data.append({
		'intend': 0,
		'account': 'Total Assets',
		'total': total_assets
	})

	data.append({})
	liability_accounts = frappe.get_all( 'StoreAccounts',
		filters = { 'root_type': ['=', 'Income', 'Liability','Equity'] }, 
		pluck = 'name'
	)

	data.append({ 'indent': 0, 'account': 'Liabilities' })
	for ledger_entry in frappe.get_all( 'StoreGL', group_by='account',
			filters={ 'account': ['in', liability_accounts] },
			fields=[ 'account', 'debit_amount']
	):
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.debit_amount,
			'parent_account': 'Liabilities'
		}) 
		total_liabilities += ledger_entry.debit_amount 
	data.append({
		'intend': 0,
		'account': 'Total Liabilities',
		'total': total_liabilities
	})
	return data
