# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from accounts.store_accounts.doctype.storeaccounts.storeaccounts import set_COA

class StoreDetails(Document):

	def on_submit(self): 
		set_COA(company_name= self.company_name)
