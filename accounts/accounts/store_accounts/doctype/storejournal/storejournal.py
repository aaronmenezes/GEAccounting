# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StoreJournal(Document):

	def before_save(self): 

		for entries in self.get('accounting_entries'): 
			self.total_debit += entries.debit
			self.total_credit += entries.credit

		if self.total_credit != self.total_debit:
			frappe.throw('Total Credit should match Total Debit')

	def on_submit(self):
		for accounting_entry in self.get('accounting_entries'):
			ledger_entry = frappe.get_doc({
				'doctype': 'StoreGL',
				'posting_date': self.date,
				'account': accounting_entry.account,
				'against':accounting_entry.account,
				'debit_amount': accounting_entry.debit,
				'credit_amount': accounting_entry.credit,
				'voucher_type': self.entry_type,
				'voucher_number': self.name
			}) 
			ledger_entry.insert()  
