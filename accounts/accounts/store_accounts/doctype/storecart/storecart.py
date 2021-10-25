# Copyright (c) 2021, aaron M and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime

class StoreCart(WebsiteGenerator):
	pass

@frappe.whitelist(allow_guest=False)
def add_item_to_cart(item_name,customer_name): 
	if customer_name==" ":
		storecustomer = frappe.get_doc('StoreCustomer',frappe.session.user)
	else :
		storecustomer = frappe.get_doc('StoreCustomer',customer_name)

	cart_list = frappe.get_all( 'StoreCart',
		filters = { 'customer': ['=', storecustomer.name], 'status': ['=', 'Open'] }
	)

	if len(cart_list)>0:
		cur_cart =  frappe.get_doc('StoreCart', cart_list[0].name)
		item_present =False
		for cart_item in cur_cart.items:
			if cart_item.item == item_name: 
				cart_item.qty += 1
				cart_item.save() 
				item_present =True
				break;
		if not item_present:
			cart_item = frappe.get_doc({
				'doctype': 'StoreCartItems',
				'item': item_name,
				'qty': 1
			})
			cur_cart.append('items', cart_item)
			cur_cart.save()
	else :
		cart_item = frappe.get_doc({
			'doctype': 'StoreCartItems',
			'item': item_name,
			'qty': 1
		})
		cur_cart = frappe.get_doc({
			'doctype': 'StoreCart',
			'customer': storecustomer.name,
			'items': [cart_item]
		})
		cur_cart.insert()
		frappe.db.commit()
	total_amount =0
	for cart_item in cur_cart.items:
		cart_item.amount = cart_item.unit_price * cart_item.qty
		total_amount += cart_item.amount
		cart_item.save()
	cur_cart.total_amount = total_amount
	cur_cart.save()
	frappe.msgprint(msg=_('Item Added'), alert=True)


@frappe.whitelist(allow_guest=False)
def checkout(current_cart,place):

	current_cart = frappe.get_doc('StoreCart',current_cart)
	sales_invoice_doc = frappe.get_doc({
		'doctype': 'StoreSalesInvoice', 
  		'customer':current_cart.customer,
  		'date':current_cart.date,
		'posting_time':datetime.now(),
		'place':place,
		'total_amount':current_cart.total_amount
		}).insert()
	frappe.db.commit()
	
	for item in current_cart.items: 
		sales_invoice_item = frappe.get_doc({
			'doctype': 'StoreInvoiceDescription', 
			'item':item.item,
			'qty':item.qty,
			'unit_price':item.unit_price,
			'amount	':item.amount
		})
		sales_invoice_doc.append('items', sales_invoice_item)
	
	sales_invoice_doc.save()
	sales_invoice_doc.submit()

	current_cart.status = "Closed"
	current_cart.save()
	return "Closed"