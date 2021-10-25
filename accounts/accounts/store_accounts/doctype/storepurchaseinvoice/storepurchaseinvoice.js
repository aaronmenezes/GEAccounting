// Copyright (c) 2021, aaron M and contributors
// For license information, please see license.txt

frappe.ui.form.on('StorePurchaseInvoice', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('StoreInvoiceDescription', { 
	unit_price:updateAmounts,
	qty: updateAmounts
});

function updateAmounts(frm, cdt, cdn){
	let row = locals[cdt][cdn]; 
	row.amount = row.qty * row.unit_price;
	refresh_field('items');

	let total = 0;
	for(let i = 0; i < frm.doc.items.length; i++) {
	    total += frm.doc.items[i].amount;
	} 
	frm.doc.total = total;
    refresh_field('total'); 
}