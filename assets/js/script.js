$('.add2cart').on('click',function(){
    
    var action = $(this).data('action')
    var id = $(this).data('id')
    console.log('Action',action,'ID',id)

    value = 0

    //adding no of items if acion is add items
    if(action==='additems'){
    value = $('#add-quantity'+id).val()
    console.log("Value",value)
    }

    //If user os logged in
    if (user!='AnonymousUser'){
        updateCart(action,id,value)
    }
    else{
        updateCartCookies(action,id,value)
    }
})



function updateCart(action,id,value){

    $.ajax({
        type: "POST",
        url: "/update_items/",
        data: JSON.stringify({'action':action,'id':id,'value':value}),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },

        success: function (data) {
            console.log("Data:",data)

            $('#cart_total_price').html('Total: $'+data['cart_total_price'])
            $('#cart_total_items').html('Items: '+data['cart_total_items'])
            
            image = data['image']
            quantity= data['quantity']
            product = data['name']
            total_price = data['total_price']
            console.log('remove',data['remove'])
            console.log('add',data['add'])


            //Updating Shopping cart Page
            if($('#shopping_cart_product_quantity'+id).val()!=undefined){
                    quantity = data['quantity']
                    shopping_cart_total_price = data['cart_total_price']
                    shopping_cart_total_price_ = data['cart_total_price']+3.0
                    shopping_cart_item_total_price = data['total_price'].toFixed(2)
                $('#shopping_cart_product-quantity'+id).val(quantity)
                $('#shopping_cart_total_price').html('$'+shopping_cart_total_price)
                $('#shopping_cart_total_price_').html('$'+shopping_cart_total_price_.toFixed(2))
                $('#shopping_cart_item_total_price'+id).html('$'+shopping_cart_item_total_price)
                
                if(quantity==0){
                $('#shopping_cart_item_row'+id).remove()
                }
              }

              add = data['add']
              remove = data['remove']


              if($('#item'+id).val()!=undefined && quantity>0){
                $('#item_quantity'+id).html('x'+quantity)
                $('#item_price'+id).html(total_price)
              }

              else if(quantity==0){
                $('#scroll_cart'+id).remove()

              }
              else{
                var item = `<li id="scroll_cart`+id+`">
                <a href="{% url 'item' id=`+id+` %}"><img src=`+image+` alt="Rolex Classic Watch" width="37" height="34"></a>
                <span id="item_quantity`+id+`" class="cart-content-count">x`+quantity+`</span>
                <strong><a id="item`+id+`" href="{% url 'item' id=`+id+` %}">`+product+`</a></strong>
                <em id="total_price`+id+`">`+total_price+`</em>
                <a href="javascript:void(0);" class="del-goods">&nbsp;</a>
                </li>`
                    $('#scroller').append(item)
              }

            console.log("ITEM:",$('#scroll_cart'+id).val())
            console.log("VALUE: ",$('#item'+id).val())
              

        }
    })    
}

function updateCartCookies(action,id,value){
    console.log("USER NOT LOGGED IN")
}