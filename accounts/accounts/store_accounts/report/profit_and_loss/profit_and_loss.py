# Copyright (c) 2013, aaron M and contributors
# License: MIT. See LICENSE

import frappe
from frappe import _

def execute(filters=None):
	data = get_data(filters)
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

def get_data(filters): 
	data = []
	total_income = 0 
	total_expense = 0 
	income_accounts = frappe.get_all( 'StoreAccounts',
		filters = { 'root_type': ['=', 'Income'] },
		pluck = 'name'
	) 
	data.append({
		'indent': 0,
		'account': 'Income',
	})

	for ledger_entry in frappe.get_all('StoreGL', group_by='account',
		filters={
			'account': ['in', income_accounts]
		},
		fields=[ 'account', 'debit_amount']): 
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.debit_amount,
			'parent_account': 'Income'
		}) 
		total_income += ledger_entry.debit_amount 
	data.append({
		'intend': 0,
		'account': 'Total Income',
		'total': total_income
	})
	data.append({})
	# expense calc
	expense_accounts = frappe.get_all( 'StoreAccounts',
		filters = { 'root_type': ['=', 'Expense'] },
		pluck = 'name'
	) 
	print(expense_accounts)
	data.append({
		'indent': 0,
		'account': 'Expense',
	})

	for ledger_entry in frappe.get_all('StoreGL', group_by='account',
		filters={
			'account': ['in', expense_accounts]
		},
		fields=[ 'account', 'credit_amount']): 
		data.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.credit_amount,
			'parent_account': 'Expense'
		}) 
		total_expense+= ledger_entry.debit_amount 
	data.append({
		'intend': 0,
		'account': 'Total Expense',
		'total': total_expense
	})
	data.append({})
	

	#  growth calc

	if total_income >= total_expense: 	# Profit
		net_profit = total_income - total_expense
		data.append({
			'account': 'Net Profit',
			'total': net_profit
		})
	else:								# Loss
		net_loss = total_expense - total_income
		data.append({
			'account': 'Net Loss',
			'total': net_loss
		})
	return data