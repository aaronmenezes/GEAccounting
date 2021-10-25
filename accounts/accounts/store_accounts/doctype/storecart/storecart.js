// Copyright (c) 2021, aaron M and contributors
// For license information, please see license.txt

frappe.ui.form.on('StoreCart', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('StoreCartItems', { 
	debit:function (frm, cdt, cdn){  
		let debit = 0;
		for(let i = 0; i < frm.doc.accounting_entries.length; i++) {
			debit += frm.doc.accounting_entries[i].debit;
		} 
		frm.doc.total_debit = debit;
		refresh_field('total_debit'); 
	},
	credit:function (frm, cdt, cdn){  
		let credit = 0;
		for(let i = 0; i < frm.doc.accounting_entries.length; i++) {
			credit += frm.doc.accounting_entries[i].credit;
		} 
		frm.doc.total_credit = credit;
		refresh_field('total_credit');  
	},
	qty:function (frm, cdt, cdn){ 
		let row = locals[cdt][cdn]; 
		row.amount = row.qty * row.unit_price;
		refresh_field('items');
		let total=0;
		for(let i = 0; i < frm.doc.items.length; i++) {
			total += frm.doc.items[i].amount;
		} 
		frm.doc.total_amount = total;
		refresh_field('total_amount');  
	}
});