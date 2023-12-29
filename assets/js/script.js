$('.add2cart').on('click', function (){
  
  var action = $(this).data('action')
  var id = $(this).data('id')
  console.log('Action', action, 'ID', id)
  
  value = 0
  //adding no of items if acion is add items
  if (action === 'additems') {
    value = $('#add-quantity' + id).val()
    console.log("Value", value)
  }

  //If user os logged in
  if (user != 'AnonymousUser') {
    updateCart(action, id, value)
  }
  else {
    updateCartCookies(action, id, value)
  }
})



function updateCart(action, id, value) {

  $.ajax({
    type: "POST",
    url: "/update_items/",
    data: JSON.stringify({ 'action': action, 'id': id, 'value': value }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },

    success: function (data) {
      console.log("Data:", data)

      $('#cart_total_price').html('Total: $' + data['cart_total_price'])
      $('#cart_total_items').html('Items: ' + data['cart_total_items'])

      image = data['image']
      quantity = data['quantity']
      product = data['name']
      total_price = data['total_price']
      console.log('remove', data['remove'])
      console.log('add', data['add'])


      //Updating Shopping cart Page
      if ($('#shopping_cart_product_quantity' + id).val() != undefined) {
        quantity = data['quantity']
        shopping_cart_total_price = data['cart_total_price']
        shopping_cart_total_price_ = data['cart_total_price'] + 3.0
        shopping_cart_item_total_price = data['total_price'].toFixed(2)
        $('#shopping_cart_product-quantity' + id).val(quantity)
        $('#shopping_cart_total_price').html('$' + shopping_cart_total_price)
        $('#shopping_cart_total_price_').html('$' + shopping_cart_total_price_.toFixed(2))
        $('#shopping_cart_item_total_price' + id).html('$' + shopping_cart_item_total_price)

        if (quantity == 0) {
          $('#shopping_cart_item_row' + id).remove()
        }
      }

      add = data['add']
      remove = data['remove']


      if ($('#item' + id).val() != undefined && quantity > 0) {
        $('#item_quantity' + id).html('x' + quantity)
        $('#item_price' + id).html(total_price)
      }

      else if (quantity == 0) {
        $('#scroll_cart' + id).remove()

      }
      else {
        var item = `<li id="scroll_cart` + id + `">
                <a href="{% url 'item' id=`+ id + ` %}"><img src=` + image + ` alt="Rolex Classic Watch" width="37" height="34"></a>
                <span id="item_quantity`+ id + `" class="cart-content-count">x` + quantity + `</span>
                <strong><a id="item`+ id + `" href="{% url 'item' id=` + id + ` %}">` + product + `</a></strong>
                <em id="total_price`+ id + `">` + total_price + `</em>
                <a href="javascript:void(0);" class="del-goods">&nbsp;</a>
                </li>`
        $('#scroller').append(item)
      }

      console.log("ITEM:", $('#scroll_cart' + id).val())
      console.log("VALUE: ", $('#item' + id).val())


    }
  })
}

function updateCartCookies(action, id, value) {
  console.log("USER NOT LOGGED IN")
}



// PRODUCT LIST FILTERS

var newBox = $('#newbox');
var saleBox = $('#salebox');
var pagerun = false

// Add event listeners to check the status when the checkboxes are clicked
newBox.add(saleBox).on('change', function () {
  checkCheckboxStatus();
},

  function checkCheckboxStatus() {
    pagerun = false
    var newChecked = newBox.prop('checked');
    var saleChecked = saleBox.prop('checked');
    var itemsPerPage = parseInt($('.selectItemNo').find(":selected").text());
    var itemsOrder = $('.selectOrder').find(":selected").text();
    var searchBox = $('#searchBox').val()
    
    numbers = rangeValues()
    value1 = numbers[0]
    value2 = numbers[1]

    console.log('CHECKBOX')
    console.log("SearchBOX",searchBox)
    console.log("NUMBERS: ", numbers)
    console.log('ItemsPerPage: ', itemsPerPage)
    console.log('ItemsOrder: ', itemsOrder)

    if (newChecked && saleChecked) {

      console.log('Both checkboxes are checked');

    } else if (newChecked) {
      console.log('New is checked');
    } else if (saleChecked) {
      console.log('Sale is checked');
    }
    else {
      console.log('Both checkboxes are not checked');
    }

    $.ajax({
      type: 'POST',
      url: '/product_list/',
      data: JSON.stringify({'searchBox':searchBox, 'value1': value1, 'value2': value2, 'newChecked': newChecked, 'saleChecked': saleChecked, 'itemsPerPage': itemsPerPage, 'itemsOrder': itemsOrder, 'source': 'filter' }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      success: function (data) {

        if (data) {
          itemsUpdate(data)
        }
      },//success

    })//ajax
  });

// GETTING THE PRICE RANGE OF SLIDER AND THEN DISPLAYING THE ITEMS IN RANGE

var value1 = 0
var value2 = 500
$("#slider-range").slider({
  range: true,
  min: value1,
  max: value2,
  values: [value1, value2], // initial values
  slide: function (event, ui) {
    value1 = parseFloat(ui.values[0])
    value2 = parseFloat(ui.values[1])

    // Update the text input with the current values
    $("#amount").val('$' + value1 + " - " + '$' + value2);
  },

  stop: function (event, ui) {
    value1 = parseFloat(ui.values[0])
    value2 = parseFloat(ui.values[1])
    var newChecked = newBox.prop('checked');
    var saleChecked = saleBox.prop('checked');
    var itemsPerPage = parseInt($('.selectItemNo').find(":selected").text());
    var itemsOrder = $('.selectOrder').find(":selected").text();
    searchBox = $('#searchBox').val()

    console.log('Slider')
    console.log("Numbers: [", value1, value2, ']')
    console.log('ItemsPerPage: ', itemsPerPage)
    console.log('ItemsOrder: ', itemsOrder)
    console.log('NewChecked: ', newChecked)
    console.log('saleChecked: ', saleChecked)

    $.ajax({
      type: 'POST',
      url: '/product_list/',
      data: JSON.stringify({'searchBox':searchBox, 'value1': value1, 'value2': value2, 'newChecked': newChecked, 'saleChecked': saleChecked, 'itemsPerPage': itemsPerPage, 'itemsOrder': itemsOrder, 'source': 'slider_range' }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      success: function (data) {
        if (data) {
          pagerun = false
          itemsUpdate(data)
        }
      }//success
    })//AJAX
  },//STOP
});//SLIDER




// GRTTING THE VALUE OF OPTION AND DISPLAYING ITEMS ACCORDING TO IT
$(".selectOption").on("change", function () {

  // Get the selected option using val()
  var value = $(this).val();
  // Get the selected option's text using :selected
  var text = $(this).find(":selected").text();

  pagerun = false
  var newChecked = newBox.prop('checked');
  var saleChecked = saleBox.prop('checked');
  numbers = rangeValues()
  value1 = numbers[0]
  value2 = numbers[1]
  searchBox = $('#searchBox').val()

  if (text.length < 4) {
    itemsPerPage = parseInt(text)
    itemsOrder = $('.selectOrder').find(":selected").text();
  }
  else {
    itemsPerPage = $('.selectItemNo').find(":selected").text();
    itemsOrder = text
  }

  console.log('SELECT OPTION')
  console.log("NUMBERS: ", numbers)
  console.log('ItemsPerPage: ', itemsPerPage)
  console.log('ItemsOrder: ', itemsOrder)

  // // Log the selected value and text
  // console.log("Selected Value: " + value);
  // console.log("Selected Text: " + text);

  $.ajax({
    type: 'POST',
    url: '/product_list/',
    data: JSON.stringify({'searchBox':searchBox, 'newChecked': newChecked, 'saleChecked': saleChecked, 'itemsPerPage': itemsPerPage, 'itemsOrder': itemsOrder, 'value1': value1, 'value2': value2, 'source': 'selectOption' }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },

    success: function (data) {
      if (data) {
        itemsUpdate(data)
      }
    }//success
  })//AJAX
});//SELECT OPTION


var page_no = 1
var pages = 1

$(document).on('click', '.page', function () {

  pagerun = true
  page_no = parseInt($(this).text())
  console.log("Page NO:", page_no)

  newChecked = $('#newbox').is(':checked');
  saleChecked = $('#salebox').is(':checked');
  itemsPerPage = parseInt($('.selectItemNo').find(":selected").text())
  itemsOrder = $('.selectOrder').find(":selected").text()
  sort_by = $('#mySelect').find(":selected").text();
  numbers = rangeValues()
  value1 = numbers[0]
  value2 = numbers[1]
  console.log("NUMBERS: ", numbers)
  searchBox = $('#searchBox').val()

  $.ajax({
    type: 'POST',
    url: '/product_list/',
    data: JSON.stringify({'searchBox':searchBox, 'value1': value1, 'value2': value2, 'saleChecked': saleChecked, 'newChecked': newChecked, 'page_no': page_no, 'itemsPerPage': itemsPerPage, 'itemsOrder': itemsOrder, 'source': 'page_filter' }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    success: function (data) {

      pages = Math.ceil(data[0]['totalItems'] / itemsPerPage)
      console.log("Pages:", pages)
      itemsUpdate(data, page_no, pages)

    },//success

  })//ajax 

})//CLICK


$('#search').on('click', function () {

  pagerun = false
  searchBoxValue = $('#searchBox').val()

  console.log("SEARCH CLICKED:", searchBoxValue)

  if (searchBoxValue != undefined)
    $.ajax({
      type: 'POST',
      url: '/search_result/',
      data: JSON.stringify({ 'searchBoxValue': searchBoxValue, 'source': 'search' }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      success: function (data) {

        console.log(data.length)

        if (data.length > 0) {
          $('#searchedFor').html("<em>" + data[0]['totalItems'] + "</em>: Search Results for <em>" + searchBoxValue + "</em>")
        } else {
          $('#searchedFor').html("<em>NO</em> Search Results for <em>" + searchBoxValue + "</em>")
        }
        $('.sidebarul').addClass('hidden')
        $('#plist-store').removeClass('active')
        $('#plist-search').removeClass('hidden')
        itemsUpdate(data)
      },//success

    })//AJAX

})//SEARCH



function itemsUpdate(data, page_no = 1, pagess = 1) {
  console.log(data)
  $('.products-filter').html('')


  console.log('totalItems:', data.length)

  var itemsPerPage = $('.selectItemNo').find(":selected").text();
  display_items = parseInt(itemsPerPage)

  var i = 1

  for (d of data) {
    dataAppender(d, i)
    i++
    if (i > display_items) { break }
  }


  if (data.length > 0) {
    if (pagerun == true) { pageUpdate(data[0]['totalItems'], page_no, pagess) }

    else { pageUpdate(data[0]['totalItems'], page_no) }
  }
  else {
    pageUpdate(0, 0)
  }


}// Function


function dataAppender(d, i) {

  id = d['id']
  name = d['name']
  image = d['image']
  price = d['price']

  item = `<div class="col-md-4 col-sm-6 col-xs-12">
      <div class="product-item">
      <div class="pi-img-wrapper">
      <img src=${image} class="img-responsive" alt="${name}">
      <div>
      <a href=${image} class="btn btn-default fancybox-button">Zoom</a>
      <a href="#${id}pop-up" class="btn btn-default fancybox-fast-view">View</a>
      </div>
      </div>
      <h3><a href="/index/${id}/item">${name}</a></h3>
      <div class="pi-price">$${price}</div>
      <a data-id={{product.id}} data-action="add" href="javascript:;" class="btn btn-default add2cart">Add to cart</a>
      </div>
      </div>`

  if (i % 3 == 1) {
    item = `<div class="row product-list"></div>` + item
  }

  if (d['sale']) {
    item = item.slice(0, -6) + '<div class="sticker sticker-sale"></div></div>'
  }// SALE

  if (d['new']) {
    item = item.slice(0, -6) + '<div class="sticker sticker-new"></div>'
  }// NEw

  $('.products-filter').append(item)
}//DataAppender

function pageUpdate(items, page_no, pagess = 1) {

  var text = $('.selectItemNo').find(":selected").text();
  display_items = parseInt(text)
  console.log('pagerun:', pagerun)
  if (pagerun == false) {
    pages = Math.ceil(items / display_items)
    console.log('pages:', pages)

  } else {
    pages = pagess
  }

  $('.pagination').html('')
  $('.pagination').append('<li><a href="javascript:;">&laquo;</a></li>')
  for (var i = 1; i <= pages; i++) {

    if (i == page_no) {
      $('.pagination').append('<li class="page" id="page' + i + '"><span>' + i + '</span></li>')
    }
    else {
      $('.pagination').append('<li class="page" id="page' + i + '"><a>' + i + '</a></li>')
    }
  }
  $('.pagination').append('<li><a href="javascript:;">&raquo;</a></li>')
  $('#currentPage').html(page_no)
  $('#totalPages').html(pages)

}//pageUpdater

function rangeValues() {
  var currentValue = $("#amount").val();
  console.log("Selected value:", currentValue);

  // Use a regular expression to match numbers in the string
  var matches = currentValue.match(/\d+/g);

  // Convert the matched strings to numbers
  var numbers = matches.map(function (match) {
    return parseInt(match, 10);
  });

  return numbers;

}//rangeValues
