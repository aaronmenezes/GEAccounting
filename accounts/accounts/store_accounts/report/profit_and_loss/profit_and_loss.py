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
		}]
	return columns

def get_data(filters): 
	data = []  
	total_income,account_summary = get_gl_amounts("credit_amount",'Income')   
	data.extend(account_summary)
	total_expense,account_summary = get_gl_amounts("debit_amount",'Expense')   
	data.extend(account_summary)  
	if total_income >= total_expense:
		net_profit = total_income - total_expense
		data.append({ 'account': 'Net Profit', 'total': net_profit })
	else:
		net_loss = total_expense - total_income
		data.append({ 'account': 'Net Loss', 'total': net_loss })
	return data

def get_gl_amounts(field_name,parent_account):
	amount = 0
	line_items=[{ 'indent': 0, 'account': parent_account}]
	accounts = frappe.get_all('StoreAccounts', filters = { 'root_type': ['=', parent_account] }, pluck = 'name')	
	for ledger_entry in frappe.get_all('StoreGL', group_by='account',
		filters={ 'account': ['in', accounts] },
		fields=[ 'account', 'sum(%s) as total_amount'%field_name,field_name]): 
		line_items.append({
			'intend': 1,
			'account': ledger_entry.account,
			'amount': ledger_entry.total_amount,
			'parent_account': parent_account
		}) 
		amount += ledger_entry.total_amount 
	line_items.append({
		'intend': 0,
		'account': 'Total %s'%parent_account,
		'total': amount
	})
	line_items.append({})
	return amount,line_items
