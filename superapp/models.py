from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=264)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    new = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    avail = models.BooleanField(default=True)
    desc = models.TextField(default="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            Praesent sit amet aliquam elit, sed ornare arcu. Nam gravida pellentesque
                            posuere. Sed sed metus in metus ullamcorper pellentesque. Maecenas tincidunt
                            mi aliquam urna consectetur vulputate. Nullam sed dolor justo. Morbi ultrices
                            enim lorem, sit amet feugiat lacus finibus eu. Proin condimentum massa enim,
                            vel tristique tortor vehicula at. Integer ornare eget elit pellentesque hendrerit.
                            Fusce vel imperdiet felis. In elit tellus, ultrices sed augue sit amet, dapibus malesuada velit.
                            Proin iaculis nisl faucibus sagittis aliquet. Donec vehicula vestibulum mauris vitae tempor.
                            Aliquam tempus, dui ac semper varius, sem felis sollicitudin risus, quis gravida tortor leo eget
                            tortor. Vestibulum mauris arcu, tristique quis ultrices id, ornare quis ipsum. Aliquam convallis
                            eleifend rhoncus. Nulla et felis sit amet arcu laoreet rhoncus ac id eros. Nulla at enim eu lacus
                            viverra viverra. Curabitur leo tellus, congue ut imperdiet quis, porta sed diam. Curabitur pretium
                            convallis faucibus. Nunc nec sem quis orci convallis pretium id in tellus""")
    
    def generate_unique_code():
        unique_code = str(uuid.uuid4().hex)[:8]  # Use the first 8 characters of the hexadecimal UUID
        return unique_code
    
    reference = models.CharField(max_length=100,default=str(generate_unique_code()))
    cat_choices = [
        (1,"MAN"),
        (2,"WOMAN"),
        (3,"KIDS"),
        (4,"OTHER"),
    ]


    category = models.IntegerField(choices=cat_choices)
    sub_choices = [
        (1,"Footwear"),
        (2,"Clothes"),
        (3,"Accessories"),
        (4,"Clearance"),
        (5,'Technology'),
        (6,'Sports'),
        (7,'Toy'),
    ]
    sub_category = models.IntegerField(choices=sub_choices)
    image = models.ImageField(upload_to='product_images', blank=True)


    @property
    def imageURL(self):

        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
    @property
    def quantity(self):
        item = OrderItem.objects.get(product=self)
        return int(item.quantity)

    def __str__(self):
        return self.name
    


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    update = models.CharField(max_length=1000,default="Order Pending!")
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)

    @property
    def cart_total_items(self):
        total = 0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            total = total+item.quantity
        return int(total)
    
    @property
    def cart_total_price(self):
        total = 0.0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total = total + (float(item.product.price)*item.quantity)
        return round(total,2)


class OrderItem(models.Model):
    items_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.product} : {int(self.quantity)}"
    
    @property
    def total_price(self):
        total = self.quantity*float(self.product.price)
        return round(total,2)


class Countries(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
