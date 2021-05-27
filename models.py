from django.db import models
import datetime as dt
from django.contrib.auth import get_user_model
# import time as dt
from random import choice
from string import ascii_letters

# Create your models here.

User = get_user_model()


class Category(models.Model):
    title = models.CharField(verbose_name='Category name', max_length=255)
    slug = models.SlugField(verbose_name='Category url', max_length=55, unique=True)
    description = models.TextField(verbose_name='Category description', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Delivery(models.Model):
    title = models.CharField(verbose_name='Delivery title', max_length=255)
    price = models.DecimalField(verbose_name='Delivery price', max_digits=9, decimal_places=2)
    max_weight = models.PositiveIntegerField(verbose_name='max_weight', default=0)
    areas = models.CharField(verbose_name='Delivery areas', max_length=25, blank=True)
    description = models.TextField(verbose_name='Delivery description', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'


class Sizes(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(verbose_name='Product size', max_length=5)
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantity', default=0)



class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name='Product categories')
    origin_url = models.URLField(verbose_name='url from store')
    title = models.CharField(verbose_name='Product name', max_length=255)
    photo = models.ImageField("General photo", upload_to="product_poster/")
    description = models.TextField(verbose_name='Product description', blank=True)
    colors = models.CharField(verbose_name='Product colors', max_length=50, blank=True)
    origin_price = models.DecimalField(verbose_name='Original product price', max_digits=9, decimal_places=2, default=0)
    price = models.DecimalField(verbose_name='My product price', max_digits=9, decimal_places=2)
    slug = models.SlugField(verbose_name='Product url', max_length=55, unique=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True)
    weight = models.PositiveIntegerField(verbose_name='Weight', default=0)
    draft = models.BooleanField(verbose_name='Draft', default=False)

    def __str__(self):
        return self.title


class ProductPhoto(models.Model):
    title = models.CharField(verbose_name='Photo title', max_length=255)
    description = models.TextField(verbose_name='Photo description', blank=True)
    image = models.ImageField("Product photo", upload_to="product_photos")
    product = models.ForeignKey(Product, verbose_name="Products", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.get_attname()


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(verbose_name='Phone number', max_length=17, default='')
    address = models.CharField(verbose_name='Address', max_length=50)
    address2 = models.CharField(verbose_name='Address line 2', max_length=50, blank=True)
    zipcode = models.CharField(verbose_name='Post index', max_length=8)
    city = models.CharField(verbose_name='City', max_length=50)
    state = models.CharField(verbose_name='State', max_length=50)
    country = models.CharField(verbose_name='User county', max_length=50)

    def __str__(self):
        return self.user.username


# class CurtProduct(models.Model):
#     user = models.ForeignKey(User, verbose_name='customer', on_delete=models.PROTECT)
#     product = models.ForeignKey(Product, verbose_name='product', on_delete=models.PROTECT)
#     cart_id = models.ForeignKey('Cart', verbose_name='cart', on_delete=models.CASCADE)
#     size = models.CharField(verbose_name='Product size', max_length=5)
#     price = models.DecimalField(verbose_name='price', max_digits=9, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#
#
# class Cart(models.Model):
#     email = models.EmailField(verbose_name='email', blank=True)
#     phone = models.CharField(verbose_name='Phone num', max_length=15, blank=True)
#     user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT, null=True, blank=True)
#     price = models.DecimalField(verbose_name='price', max_digits=9, decimal_places=2, null=True)
#     address = models.TextField(verbose_name='Delivery address', blank=True)
#     comment = models.TextField(verbose_name='Comment', blank=True)
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#     weight = models.PositiveIntegerField(verbose_name='Weight', default=0)
#     delivery = models.ForeignKey(Delivery, verbose_name='Delivery', on_delete=models.PROTECT, null=True)
#
#     def __str__(self):
#         return str(self.id)


class Review(models.Model):
    prod_id = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    review = models.CharField(verbose_name='Review', max_length=500)
    photo = models.ImageField("Reviews photo", upload_to="product_reviews/")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.prod_id.title


class OrderStatus(models.Model):
    name = models.CharField(verbose_name='Status name', max_length=250)

    def __str__(self):
        return self.name

class Order(models.Model):
    email = models.EmailField(verbose_name='email', blank=True)
    phone = models.CharField(verbose_name='Phone num', max_length=15, blank=True)
    status = models.ForeignKey(OrderStatus, verbose_name='order status', on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(verbose_name='price', max_digits=9, decimal_places=2, null=True)
    address = models.TextField(verbose_name='Delivery address', blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    weight = models.PositiveIntegerField(verbose_name='Weight', default=0)
    delivery = models.ForeignKey(Delivery, verbose_name='Delivery', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.id)




class OrderProduct(models.Model):
    user = models.ForeignKey(User, verbose_name='customer', on_delete=models.PROTECT)
    product = models.ForeignKey(Product,verbose_name='product', on_delete=models.PROTECT)
    order_id = models.ForeignKey(Order,verbose_name='order', on_delete=models.CASCADE)
    size = models.CharField(verbose_name='Product size', max_length=5)
    price = models.DecimalField(verbose_name='price', max_digits=9, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.product.title

class AccUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    acc_link = models.CharField(verbose_name='acceptance link', max_length=250, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def new_link(lenght=12):
        link_string = ''.join(choice(ascii_letters) for i in range(lenght))
        return link_string
