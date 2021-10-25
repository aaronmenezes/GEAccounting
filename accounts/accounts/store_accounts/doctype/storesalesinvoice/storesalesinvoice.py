# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StoreSalesInvoice(Document):
	def before_save(self):
		pass
	
	def on_submit(self):

		store_name = frappe.get_doc('StoreDetails') 
		sales_accounts = frappe.get_all('StoreAccounts',filters = {'account_type': ['=', 'Income Account'] }, pluck = 'name' )
		debtors_accounts = frappe.get_all( 'StoreAccounts', filters = {'account_type': ['=', 'Receivable'] },pluck = 'name' )
	  
		if len(sales_accounts) == 0:
			frappe.throw(_('Income account not set'))
			return
		if len(debtors_accounts) == 0:
			frappe.throw(_('Receivable account not set'))
			return 

		ledger_entry_doc1 = frappe.get_doc({
			'doctype': 'StoreGL',
			'posting_date': self.date,
			'account': sales_accounts[0],
			'debit_amount': self.total,
			'credit_amount': 0,
			'voucher_type': 'Sales Invoice',
			'voucher_no': self.name,
			'company': store_name.name,
			'against':self.name 
		})

		ledger_entry_doc2 = frappe.get_doc({
			'doctype': 'StoreGL',
			'posting_date': self.date,
			'account': debtors_accounts[0],
			'debit_amount': 0,
			'credit_amount': self.total,
			'voucher_type': 'Sales Invoice',
			'voucher_no': self.name,
			'company': store_name.name,
			'against':self.name
		})

		ledger_entry_doc1.insert()
		ledger_entry_doc2.insert()
		self.reload()
