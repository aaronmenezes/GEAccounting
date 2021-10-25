import frappe
from frappe import _
import accounts.store_accounts.doctype.storecustomer.storecustomer as storeCustomer

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Log in."), frappe.PermissionError) 

    customer_name = storeCustomer.get_customer_details(frappe.session.user)
    context.customer_name = customer_name.name 
    context.store_name = frappe.get_doc('StoreDetails').store_name   

    cart_list = frappe.get_all('StoreCart',filters = { 'customer': ['=', customer_name.name], 'status': ['=', 'Open'] })    
    if len(cart_list) == 0:
        context.current_cart = None
        context.cart_items = [] 
    else : 
        context.current_cart =  frappe.get_doc('StoreCart', cart_list[0].name) 
        context.cart_items =  frappe.get_doc('StoreCart', cart_list[0].name).items 
    return context