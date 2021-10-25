# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt


import json
import frappe
from frappe.utils.nestedset import NestedSet, rebuild_tree

class StoreAccounts(NestedSet):

	def set_root_type():
		if self.parent_account:
			parent_account = frappe.db.get_value("StoreAccounts", self.parent_account,
				["root_type"], as_dict=1) 
			if par.root_type:
				self.root_type = par.root_type
			else :
				self.root_type = self.account_name  

	def on_submit(self):
		self.root_type = set_root_type()
