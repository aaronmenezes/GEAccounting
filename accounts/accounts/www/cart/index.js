function goBack(){
    window.history.back();
}

function checkout(current_cart_name){ 
    frappe.call({
        method: "accounts.store_accounts.doctype.storecart.storecart.checkout",
        args: {
            "current_cart": current_cart_name,
            "place": document.getElementById('cityName').value
        }
    }) 
}