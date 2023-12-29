from django.shortcuts import render
from superapp.models import *
import json
from django.http import JsonResponse

def base(request):

    products_new = Product.objects.filter(new=True)
    context = {'products_new':products_new}
        
    return render(request,'base.html',context)


def index(request):
    products_sale = Product.objects.filter(sale=True)
    products_sports = Product.objects.filter(sub_category=6)

    context = {
        'products_sale':products_sale,
        'products_sports':products_sports,

        }
    return render(request,'index.html',context)

def item(request,id):

    product = Product.objects.get(id=id)

    item = OrderItem.objects.filter(product=product)
    if item.exists():
        item = item.first()
    else:
        item = 0

    context={'product':product,'item':item}
    return render(request,'item.html',context)

def kids(request):

    products = Product.objects.filter(category=3)

    item = []
    context={'products':products,'item':item}
    return render(request,'kids.html',context)

def about(request):
    return render(request,'about.html')

def account(request):
    return render(request,'account.html')

def checkout(request):
    countries = Countries.objects.all()

    print(countries)

    context = {'countries':countries}
    return render(request,'checkout.html',context)

def contacts(request):
    return render(request,'contacts.html')

def faq(request):
    return render(request,'faq.html')

def goods_compare(request):
    return render(request,'goods-compare.html')

def privacy_policy(request):
    return render(request,'privacy-policy.html')

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math


def search(text,product):
    find = False
    text = text.lower()
    if text in product.name.lower() or text in product.desc.lower():
        find = True
    return find

def product_list(request,page=1):
    
    products = Product.objects.all()
    items = Product.objects.all()
    paginator = Paginator(items, 10)   # 10 items per page

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)


    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source = data.get('source')
            newChecked = data['newChecked']
            saleChecked = data['saleChecked']
            value1 = data.get('value1')
            value2 = data.get('value2')
            itemsperPage = data['itemsPerPage']
            itemsOrder = data['itemsOrder']
            print('source:',source)
                

            if(newChecked and saleChecked):
                products = Product.objects.filter(new=True,sale=True)

            elif(newChecked):
                products = Product.objects.filter(new=True)

            elif(saleChecked):
                products = Product.objects.filter(sale=True)

            products = products.filter(price__gte=value1,price__lte=value2)
                
            if itemsOrder.lower() == 'name (a - z)':
                products = products.order_by('name')
            elif itemsOrder.lower() == 'name (z - a)':
                products = products.order_by('-name')
            elif itemsOrder.lower() == 'price (low > high)':
                products = products.order_by('price')
            elif itemsOrder.lower() == 'price (high > low)':
                products = products.order_by('-price')

            totalProducts = products

            product_list = []
            if products.exists() and source!='page_filter':
                for product in products:
                    product_list.append({
                            'id':product.id,
                            'name':product.name,
                            'price': product.price,
                            'image': product.imageURL,
                            'sale':product.sale,
                            'new':product.new,
                            'totalItems':len(totalProducts)
                            })
            
            elif source == 'page_filter':
                page_no = data.get('page_no')

                # products = totalProducts.filter(id__gt=(itemsperPage)*(page_no-1),id__lte=(itemsperPage)*(page_no))

                i = 1
                for product in products:
                    if i<=page_no*itemsperPage and i>(page_no-1)*itemsperPage:
                            product_list.append({
                                'id':product.id,
                                'name':product.name,
                                'price': product.price,
                                'image': product.imageURL,
                                'sale':product.sale,
                                'new':product.new,
                                'totalItems':len(totalProducts)
                            })
                    i=i+1
                    

            return JsonResponse(product_list,safe=False)

        except Exception as e:
            print(e)

    context = {'products':products,'items':current_page}
        
    return render(request,'product-list.html',context)

def search_result(request,page=1):
    products = Product.objects.all()
    product_list = []
    message = ''

    if request.method=='POST':
            searchItem = request.POST['searchBox']

            if len(searchItem)>3:
                for product in products:
                    if search(searchItem,product):
                        product_list.append({
                        'id':product.id,
                        'name':product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                        'sale':product.sale,
                        'new':product.new,
                    })
                
            if len(product_list)>0:
                product_list[0]['totalItems'] = len(product_list)
            message = searchItem


            # return JsonResponse(product_list,safe=False)
                
            print(product_list)

    paginator = Paginator(product_list, 10)   # 10 items per page
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
            
    context = {'products':product_list,'items':current_page,
               'message':message}
    return render(request,'search-result.html',context)


def shopping_cart(request):
    return render(request,'shopping-cart.html')

def standard_forms(request):
    return render(request,'standard-forms.html')


def terms_conditions(request):
    return render(request,'terms-conditions.html')


def wishlist(request):
    return render(request,'wishlist.html')

def update_items(request):

    if request.method=='POST':
        customer = request.user.customer
        try:
            data = json.loads(request.body)

            id = data['id']
            action = data['action']
            value = data['value']
            value = float(value)
            print(action,id,value)


            orders = Order.objects.filter(customer=customer,complete=False)
                
            if orders.exists():
                order = orders.first()
            else:
                order = Order.objects.create(customer=customer,complete=False)

            product = Product.objects.get(id=id)
            items = OrderItem.objects.filter(order=order,product=product)

            if items.exists():
                item = items.first()
                add = False
            else:
                item = OrderItem.objects.create(order=order,product=product,quantity=0)
                add = True

            if action == 'add':
                item.quantity += 1
            elif action == 'remove':
                item.quantity = max(item.quantity - 1, 0)
            elif action == 'additems':
                if value==0:
                    item.quantity = 0
                elif value<item.quantity:
                    item.quantity=value
                else:
                    item.quantity = item.quantity + (value-item.quantity)

            item.save()
            order.save()

            if item.quantity==0:
                item.delete()
                remove = True
                add = False
            else:
                remove = False


            cart_total_items = order.cart_total_items
            cart_total_price = round(order.cart_total_price,2)
            quantity = int(item.quantity)
            image = product.imageURL
            name = product.name
            total_price = round(item.total_price,2)

            mydict = {
                    'name':name,
                    'image':image,
                    'total_price':total_price,
                    'quantity':quantity,
                    'remove': remove,
                    'add': add,
                    'cart_total_items': cart_total_items,
                    'cart_total_price': cart_total_price,
                }

            return JsonResponse(mydict)

        except Exception as e:
            print(e)
            return JsonResponse("ERROR",safe=False)
    
    return JsonResponse("Item was added", safe=False)
