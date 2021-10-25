# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class StoreCustomer(Document):
	pass 

@frappe.whitelist(allow_guest=False)
def get_customer_details(user_name):
	session_user = frappe.get_doc('User', user_name) 
	customers = frappe.get_all('StoreCustomer', filters={'full_name': ['=', session_user.full_name]})

	if len(customers) == 0:  
		customer = frappe.get_doc({
            'doctype': 'StoreCustomer',
            'full_name':session_user.full_name,
			'date_of_entry':datetime.now()
        })
		customer.insert()
		frappe.db.commit()
	else: 
		customer = customers[0] 
	return customer

