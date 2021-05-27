from django.contrib import admin
from .models import Category, Product, ProductPhoto, Delivery, Customer, Review, OrderStatus, Order,\
    OrderProduct, Sizes
from django.utils.safestring import mark_safe

# Register your models here.



class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 1

class ProductSizesInline(admin.StackedInline):
    model = Sizes
    readonly_fields = ['quantity', 'size']
    extra = 1
    can_delete = False

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'origin_price', 'price', 'mark_up', 'get_link', 'get_img')
    inlines = [ProductSizesInline, ProductPhotoInline]
    save_as = True
    save_on_top = True

    def get_img(self, obj):
        return mark_safe(f'<img src={obj.photo.url} height="120">')

    def get_link(self, obj):
        return mark_safe(f'<a target="_blank" href="{obj.origin_url}">link to origin product</a>')

    def mark_up(self, obj):
        my_price = obj.price
        orig_price = obj.origin_price
        markup = my_price/orig_price
        return f'{round(markup*100,2)} %'

    # get_img.short_description = 'Image' / don't delete it !!!


@admin.register(Order)
class AdminProduct(admin.ModelAdmin):
    save_on_top = True
    fields = ['status', 'comment','date', 'weight', 'mdelivery', 'address', 'user', 'email', 'phone', 'price']
    readonly_fields = ['date', 'weight', 'mdelivery', 'address', 'user', 'email', 'phone', 'price']
    list_display = ('id', 'status', 'date', 'email', 'price')


    def mdelivery(self, obj):

        return f'{obj.delivery},_____price: {obj.delivery.price}'

    def save_model(self, request, obj, form, change):
        # insert that i wont to do
        super().save_model(request, obj, form, change)



# @admin.register(Curt)
# class AdminCart(admin.ModelAdmin):
#     list_display = ('user_cart',)


@admin.register(Sizes)
class AdminSizes(admin.ModelAdmin):
    list_display = ('product', 'product_id', 'size', 'quantity')
    search_fields = ['product__title']
    fields = ['product', 'size', 'quantity']

    def product_id(self, obj):
        return obj.product.id


@admin.register(Delivery)
class AdminSizes(admin.ModelAdmin):
    list_display = ('title', 'price', 'max_weight', 'areas')
    save_as = True

# @admin.register(ProductPhoto)
# class AdminProductPhoto(admin.ModelAdmin):
#     list_display = ()


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(OrderStatus)
admin.site.register(OrderProduct)

