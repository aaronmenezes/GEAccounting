// Copyright (c) 2021, aaron M and contributors
// For license information, please see license.txt

frappe.ui.form.on('StoreJournal', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('StoreAccountingEntries', { 
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
	}
});