# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StorePurchaseInvoice(Document):
	
	def before_save(self):
		pass
	
	def on_submit(self):
		store_name = frappe.get_doc('StoreDetails') 
		expense_accounts = frappe.get_all('StoreAccounts',filters = {'account_type': ['=', 'Income Account'] }, pluck = 'name' )
		creditor_accounts = frappe.get_all( 'StoreAccounts', filters = {'account_type': ['=', 'Payable'] },pluck = 'name' )

		if len(expense_accounts) == 0:
			frappe.throw(_('Expense account not set'))
			return
		if len(creditor_accounts) == 0:
			frappe.throw(_('Payable account not set'))
			return  

		if self.total ==0:
			for item in self.items: 
				item.amount = item.qty*item.unit_price
				self.total += item.amount
		
		ledger_entry_doc1 = frappe.get_doc({
			'doctype': 'StoreGL',
			'posting_date': self.date,
			'account': expense_accounts[0],
			'debit_amount': self.total,
			'credit_amount': 0,
			'voucher_type': 'Purchase Invoice',
			'voucher_no': self.name,
			'company': store_name.store_name,
			'against':self.name 
		}) 
		ledger_entry_doc2 = frappe.get_doc({
			'doctype': 'StoreGL',
			'posting_date': self.date,
			'account': creditor_accounts[0],
			'debit_amount': 0,
			'credit_amount': self.total,
			'voucher_type': 'Purchase Invoice',
			'voucher_no': self.name,
			'company': store_name.store_name,
			'against':self.name
		})

		ledger_entry_doc1.insert()
		ledger_entry_doc2.insert()
		self.reload()

