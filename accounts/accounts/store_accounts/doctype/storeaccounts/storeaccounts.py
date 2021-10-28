# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import json
import os

import frappe
from frappe.utils.nestedset import NestedSet, rebuild_tree 

class StoreAccounts(NestedSet):
	pass

def set_COA(company_name):
	chart_schema = get_chart_template()
	accounts = [] 
	field_list = ["account_name", "account_number", "account_type", "root_type", "is_group"]

	def parse_template_file(children,parent,root_type,root_node=False):
		for account_name,child in children.items():
			if account_name not in field_list : 
				if root_node:
						root_type = child.get("root_type")
				if child.get("is_group"):
					is_group = child.get("is_group")
				elif len(set(child.keys()) - set(["account_type", "root_type", "is_group"])):
					is_group = 1
				else:
					is_group = 0
				
				account = frappe.get_doc({
							"doctype": "StoreAccounts",
							"account_name": account_name, 
							"parent_storeaccounts": parent,
							"is_group": is_group,
							"root_type": root_type, 
							"account_type": child.get("account_type")
						})
				account.insert() 
				accounts.append(account_name)
				parse_template_file(child, account.name, root_type)

	parse_template_file(chart_schema,None,None,True)
	rebuild_tree("StoreAccounts", "parent_storeaccounts")

def get_chart_template(): 
	with open(os.path.join(os.path.dirname(__file__), "standard_chart_of_accounts.json"), "r") as chart_file:
		chart = chart_file.read()
		return json.loads(chart)