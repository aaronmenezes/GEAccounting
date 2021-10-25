
set_customer_name()

async function set_customer_name() { 
    session_user = await get_user(); 
    console.log(session_user)
};

async function get_user() {
    let url = document.location.origin + '/api/method/frappe.auth.get_logged_user';
	return fetch(url)
		.then((res) => res.message);
} 

function addItemToCart(title){    
    frappe.call({
        method: "accounts.store_accounts.doctype.storecart.storecart.add_item_to_cart",
        args: {
            "item_name": title,
            "customer_name":" " 
        }
    }) 
}