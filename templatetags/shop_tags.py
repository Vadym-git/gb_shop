from django import template
from shop.models import Category
from shop.views import web_server

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    return categories


@register.simple_tag()
def get_server():
    return web_server


@register.simple_tag()
def log_or_not():
    if True:
        return 'My account'
    # return 'Sign In'
