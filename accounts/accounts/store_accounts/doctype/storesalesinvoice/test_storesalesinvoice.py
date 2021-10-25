# Copyright (c) 2021, aaron M and Contributors
# See license.txt

import frappe
import unittest
import random
from datetime import datetime	

class TestStoreSalesInvoice(unittest.TestCase):
	def tearDown(self):
		frappe.db.rollback()
	
	def setUp(self):
		frappe.set_user("Administrator")
	
	def gen_dummy_invoice(self):
		cart_items = frappe.get_all('StoreItem', fields=['name', 'sell_price'])[0:5]	

		sales_invoice_items = []

		total_amount = 0
		for item in cart_items:  
			qty=random.randint(0, 10)	
			cart_item = frappe.get_doc({
				'doctype': 'StoreInvoiceDescription',
				'item': item.name,
				'qty': qty
			})
			sales_invoice_items.append(cart_item)
			total_amount += qty * item.sell_price

		sales_invoice = frappe.get_doc({
			'doctype': 'StoreSalesInvoice',
			'company': 'Gada Electronics',
			'customer': 'Administrator',
			'posting_date': datetime.now().date(),
			'items': sales_invoice_items,
			'place': 'narnia'
		})
		sales_invoice.insert()
		sales_invoice.submit()
		frappe.flags.test_events_created = True

		return (sales_invoice.name, total_amount)
	
	def test_gl_count(self):
		ledger_entries_count = frappe.db.count('StoreGL')
		print('before count: {}'.format(ledger_entries_count))
		self.gen_dummy_invoice()
		ledger_entries_count_new = frappe.db.count('StoreGL')
		print('after count: {}'.format(ledger_entries_count_new))

		ledger_entries_created = ledger_entries_count_new - ledger_entries_count
		self.assertEqual(ledger_entries_created, 2, "Expected 2 ledger entries for each sales invoice. but created: {}".format(ledger_entries_created))
 