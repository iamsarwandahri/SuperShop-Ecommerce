from django.shortcuts import render
from superapp.models import *
import json
from django.http import JsonResponse
from django.db.models.functions import Length


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

    # item = OrderItem.objects.filter(product=product)
    # if item.exists():
    #     item = item.first()
    # else:
    #     item = 0

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

def index_header_fix(request):
    return render(request,'index-header-fix.html')

def index_light_footer(request):
    return render(request,'index-light-footer.html')

def privacy_policy(request):
    return render(request,'privacy-policy.html')

from django.db.models import Q
from django.forms.models import model_to_dict

def product_list(request):
    products = Product.objects.all()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            newChecked = data['newChecked']
            saleChecked = data['saleChecked']

            # print(newChecked,saleChecked)

            if(newChecked and saleChecked):
                products = Product.objects.filter(Q(new=True) | Q(sale=True))


            elif(newChecked):
                products = Product.objects.filter(new=True)

            elif(saleChecked):
                products = Product.objects.filter(new=True)
            
            product_list = []
            if products.exists():
                for product in products:
                    product_list.append({
                        'id':product.id,
                        'name':product.name,
                        'price': product.price,
                        'image': product.imageURL,
                        'sale':product.sale,
                        'new':product.new,
                         })

            return JsonResponse(product_list,safe=False)

        except Exception as e:
            print(e)

    context = {'products':products}
        
    return render(request,'product-list.html',context)

def search_result(request):
    return render(request,'search-result.html')

def shopping_cart_null(request):
    return render(request,'shopping_cart-null.html')

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



def price_filter(request):

    product_list = []
    value1 = 0
    value2 = 500
    sort_by = 'name'
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source = data.get('source')
            print(source)
            print('Bame ')
            
            if source == 'price_range':
                value1 = data.get('value1')
                value2 = data.get('value2')
                print(value1,value2)

                print(value1,value2)
                products = Product.objects.filter(price__gt=value1,price__lt=value2)

            elif source == 'display_order':
                sort_by = data.get('sort_by')

                if len(sort_by)<4:
                    number = int(sort_by)

                    products = Product.objects.filter(id__lt=number+1)

                elif sort_by.lower() == 'name (a - z)':
                    products = Product.objects.order_by('name')
                elif sort_by.lower() == 'name (z - a)':
                    products = Product.objects.order_by('-name')
                elif sort_by.lower() == 'price (low > high)':
                    products = Product.objects.order_by('price')
                elif sort_by.lower() == 'price (high > low)':
                    products = Product.objects.order_by('-price')
                else:
                    products = Product.objects.all()

            for product in products:
                product_list.append({
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'image':product.imageURL,
                'new':product.new,
                'sale':product.sale,
                })


        except Exception as e:
            print(e)

    return JsonResponse(product_list,safe=False)