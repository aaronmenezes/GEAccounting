import frappe
from frappe import _
import accounts.store_accounts.doctype.storecustomer.storecustomer as storeCustomer

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("Log in"), frappe.PermissionError)

    if frappe.session.user == "Administrator": 
        customer_list = frappe.get_all('StoreCustomer', fields=['name', 'full_name'])
        context.customer_list = customer_list
    context.customer_name = storeCustomer.get_customer_details(frappe.session.user).name 
    context.store_name = frappe.get_doc('StoreDetails').store_name
    context.store_items = frappe.get_all('StoreItem',fields=['name','qty','image','desc','rating',"sell_price"]) 
    return context