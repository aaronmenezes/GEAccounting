function getItemDetails(item){  
    window.location.href = "http://accounts.test:8000/items/" + item.name;
}
var selected_item=undefined
function addItemToCart(item,customer_name){ 
    selected_item = item
    if(customer_name=="Administrator"){
        $('#modal').modal('show')
    }else{
        frappe.call({
            method: "accounts.store_accounts.doctype.storecart.storecart.add_item_to_cart",
            args: {
                "item_name": item.name,
                "customer_name":customer_name
            }
        }) 
    }
}

function addToCustomerCart(){
    frappe.call({
            method: "accounts.store_accounts.doctype.storecart.storecart.add_item_to_cart",
            args: {
                "item_name":selected_item.name,
                "customer_name":$('#customerSelect').find(":selected").text()
            }
        }) 

}