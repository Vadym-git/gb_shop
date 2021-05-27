from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Product, Category, Customer, Review, Order, OrderProduct, OrderStatus, AccUser, Sizes, \
    Delivery as Deliveries
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, response
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import json
import stripe
from django.db.models import F
from django.core.mail import send_mail
from django.db import DatabaseError, transaction, IntegrityError
from countries import countries, eucountries
from django.db.models.signals import pre_save

# Create your views here.
web_server = '/'
stripe.api_key = 'sk_test_+++++++++++++++++++++++++++'
# ключь более не действителен


class Index(View):
    def get(self, request):
        products = Product.objects.filter(draft=False)
        return render(request, 'shop/index.html', {'product_list': products})


class CategoryPage(View):
    def get(self, request, slug):
        category_id = Category.objects.all().filter(slug=slug)
        category_id = category_id[0]
        category_name = category_id.title
        items = Product.objects.filter(draft=False).filter(category=category_id)
        return render(request, 'shop/category.html',
                      {'items': items, 'category_name': category_name, 'web_server': web_server})


class ProductPage(View):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except:
            return HttpResponseRedirect(reverse('shop:index'))
        reviews = Review.objects.filter(prod_id=product)
        product_size_data = Sizes.objects.filter(product=product)
        quantity = product_size_data.values('quantity')
        sizes = product_size_data.values('size')
        sizes = [i.get('size') for i in sizes]
        quantity = sum([i.get('quantity') for i in quantity])
        if quantity == 0:
            product.draft = True
        return render(request, 'shop/product.html', {'product': product, 'sizes': sizes, 'reviews': reviews,
                                                     'quantity': quantity})


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            # get user data
            user = request.user
            try:
                customer = (Customer.objects.filter(user=user))[0]
            except:
                pass
            try:
                first_name = user.first_name
                second_name = user.last_name
            except:
                first_name, second_name = '', ''
            try:
                email = user.email
            except:
                email = ''
            try:
                address = customer.address
                address2 = customer.address2
                city = customer.city
                state = customer.state
                country = customer.country
                zipcode = customer.zipcode
                telephone_num = customer.phone_number
            except:
                address, address2, city, state, country, zipcode, telephone_num = '', '', '', '', '', '', ''
            return render(request, 'shop/login.html', {'answer': 'auth', 'first_name': first_name,
                                                       'second_name': second_name, 'email': email,
                                                       'address': address, 'address2': address2,
                                                       'city': city, 'state': state, 'country': country,
                                                       'zipcode': zipcode,
                                                       'phone_num': telephone_num,
                                                       'countries': countries})  # don't delete answer !!!
        return render(request, 'shop/login.html', {'country': countries})


class RegAccountPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('shop:login'))
        return render(request, 'shop/registration.html')

    def post(self, request):
        reg_data = request.POST
        email = reg_data['email']
        password = reg_data['password']
        password_confirmation = reg_data['password_confirmation']
        if password != password_confirmation:
            return render(request, 'shop/registration.html', {'message': 'Passwords not correct'})
        try:
            chek_user = User.objects.get(email=email)
            if chek_user:
                return render(request, 'shop/registration.html', {'message': f'This email: {email} is reg allready'})
        except:
            # make reg accaption link
            reg_link = AccUser()
            activation_link = AccUser.new_link(24)
            reg_link.acc_link = activation_link
            try:
                reg_link.save()
                user = User.objects.create_user(username=email, email=email, password=password, is_active=False)
                reg_link.user = user
                customer = Customer()
                customer.user = user
                customer.save()
                reg_link.save()
            except:
                return render(request, 'shop/registration.html', {'message': 'Oops something went wrong, try again'})
            try:

                send_mail(
                    'First email',
                    f'Here is the your activation link:\nhttp://127.0.0.1:8000/acceptance_of_reg/{activation_link}.',
                    from_email='noreply@ohgirls.eu',
                    recipient_list=['vadim.melnichenko@gmail.com'],  # change email !!!!! =================
                    auth_user='vadym@ohgirls.eu',
                    auth_password='VadiM23071990*',  # encrypt password on server =================================
                    fail_silently=False,
                )
            except:
                pass
            slug = 'newreg'
            return HttpResponseRedirect(reverse('shop:acc_reg', args=[slug]))


class AccReg(View):  # acceptance_of_reg account
    def get(self, request, slug):
        ref_link = slug
        if slug == 'newreg':
            text = 'We sent reg link on your email'
            return render(request, 'shop/acc_reg.html', {'text': text, 'img': 'sentlink.png'})
        try:
            check_reg_user = AccUser.objects.get(acc_link=ref_link)
            user = check_reg_user.user
            user.is_active = True
            user.save()
            text = 'Well Done, now you can login'
            return render(request, 'shop/acc_reg.html', {'text': text, 'confirmation': True, 'img': 'login.png'})
        except:
            text = 'Oops, wrong link'
            return render(request, 'shop/acc_reg.html', {'text': text, 'img': 'oops.png'})


class CartPage(View):
    # with transaction.atomic():
    # quant_prod = Sizes.objects.get(product=product)
    # quant_prod.quantity = F('quantity') - 1
    # quant_prod.save()
    @staticmethod
    def chec_cart(request):
        try:
            products = request.COOKIES['cart']  # trying get the cookie
            products = json.loads(products)
        except:
            return render(request, 'shop/cart.html')
        # validation cart objects
        cart, cookies, price, weight = [], [], [], []
        try:
            for i in products:
                id = int(i[0])
                size = i[1]
                product = Product.objects.get(pk=id)
                if product.draft == True:
                    continue
                item = [product, size]
                cook = [id, size]
                cart.append(item)
                cookies.append(cook)
                price.append(product.price)
        except:
            cart = cookies = price = weight = []
        return cart, cookies, price, weight

    def get(self, request):
        try:
            cart, cookies, price, weight = CartPage.chec_cart(request)
        except:
            cart = cookies = price = weight = []
        return render(request, 'shop/cart.html', {'cart': cart, 'cookies': json.dumps(cookies), 'price': sum(price)})

    def post(self, request):
        index = request.POST['index']
        cart, cookies, price, weight = CartPage.chec_cart(request)
        try:
            index = int(index)
        except:
            cart = cookies = []
            return HttpResponseRedirect(reverse('shop:cart'),
                                        {'cart': cart, 'cookies': json.dumps(cookies), 'price': 0})
        try:
            cart.pop(index - 1)
            cookies.pop(index - 1)
            price.pop(index - 1)
        except:
            pass
        return render(request, 'shop/cart.html', {'cart': cart, 'cookies': json.dumps(cookies), 'price': sum(price)})


class CheckoutPage(View):

    def get(self, request):
        return HttpResponseRedirect(reverse('shop:cart'))

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            name = f'{str(user.first_name)} {user.last_name}'
            email = user.email
            try:
                customer = Customer.objects.get(user_id=user)
                address = customer.address
                address2 = customer.address2
                city = customer.city
                state = customer.state
                country = customer.country
                zipcode = customer.zipcode
                phone = customer.phone_number
            except:
                address = address2 = city = state = country = zipcode = phone = ''

            return render(request, 'shop/checkout.html',
                          {'email': email, 'name': name, 'address': address,
                           'address2': address2, 'city': city, 'state': state,
                           'country': country, 'zipcode': zipcode, 'phone': phone,
                           'countries': countries})

        return render(request, 'shop/checkout.html', {'countries': countries})


class AccAddress(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('shop:cart'))

    def post(self, request):

        try:
            products = request.COOKIES['cart']  # trying get the cookie
            products = json.loads(products)
        except:
            return render(request, 'shop/cart.html')
        # validation cart objects
        cart, cookies, price, weight = [], [], [], []
        products_list_for_page = []
        try:
            for i in products:
                id = int(i[0])
                size = i[1]
                product = Product.objects.get(pk=id)
                if product.draft == True:
                    continue
                products_list_for_page.append(product)
                item = [product, size]
                cook = [id, size]
                cart.append(item)
                cookies.append(cook)
                price.append(product.price)
                weight.append(product.weight)
        except:
            return render(request, 'shop/cart.html')

        data = request.POST
        address = (f'{data["name"]}\n{data["address"]}\n{data["address2"]}\n{data["city"]}\n{data["state"]}\n'
                   f'{data["country"]}\n{data["zipcode"]}').strip()
        email = data['email']
        phone = data['phone']
        comment = data['comment']
        # get delivery method
        if data['country'] in ['Ireland', 'Northern Ireland']:
            area = 1
        elif data['country'] == 'United Kingdom':
            area = 2
        elif data['country'] in eucountries:
            area = 3
        else:
            area = 4

        delivery_methods = Deliveries.objects.filter(areas=area).filter(max_weight__gte=sum(weight)).order_by('price')

        try:
            delivery_price = delivery_methods[0].price
        except:
            # отправить на страницу ошибки и сообщить что заказ слишком тяжелый
            text = f'To heavy'
            return render(request, 'shop/error.html', {'text': text, 'img': 'oops.png'})

        if sum(price) >= 50:
            delivery_price = 0
        total_price = sum(price) + delivery_price

        return render(request, 'shop/accaddress.html',
                      {'email': email, 'phone': phone,
                       'address': address.replace('\n', '<br>').replace('<br><br>', '<br>'),
                       'comment': comment, 'delivery': delivery_methods[0].id, 'price': sum(price),
                       'products': products_list_for_page, 'tprice': total_price, 'dprice': delivery_price})


def account(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except Exception:
        try:
            request.POST['logout']
        except Exception:
            return render(request, 'shop/login.html', {'log_or_not': 'Something went wrong'})
        logout(request)
        return render(request, 'shop/login.html', {'log_or_not': 'You logged out'})

    try:
        username = User.objects.get(email=email)
    except Exception:
        username = 'fake'

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        request.session.set_expiry(900)
        # try:
        #     Cart.objects.filter(user_cart_id=user.id)[0]
        # except:
        #     cart = Cart(user_cart_id=user.id)
        #     cart.save()
        return HttpResponseRedirect(reverse('shop:login'))
    return render(request, 'shop/login.html', {'log_or_not': 'Please check your login or password'})


def change_data(request):
    post = request.POST
    if request.user.is_authenticated:
        try:
            name = post['name']
            sec_name = post['second_name']
            address = post['address']
            address2 = post['address2']
            city = post['city']
            country = post['country']
            zipcode = post['zipcode']
            phone = post['phone_num']
            state = post['state']
        except:
            name = ''
            sec_name = ''
            address = ''
            address2 = ''
            city = ''
            country = ''
            zipcode = ''
            phone = ''
            state = ''
        user = request.user
        try:
            castomer = (Customer.objects.filter(user=user))[0]
        except:
            castomer = Customer()
            castomer.user = user
        user.first_name = name
        user.last_name = sec_name
        castomer.address = address
        castomer.address2 = address2
        castomer.city = city
        castomer.country = country
        castomer.zipcode = zipcode
        castomer.phone_number = phone
        castomer.state = state
        user.save()
        castomer.save()
        return HttpResponseRedirect(reverse('shop:login'))
    return render(request, 'shop/login.html')


def add_review(request):
    post = request.POST
    slug = post['slug']
    if request.user.is_authenticated:
        p_id = post['id']
        review = post['review']
        try:
            photo = request.FILES['photo']
        except:
            photo = 'product_reviews/fivicon.png'
        user = request.user
        new_review = Review()
        new_review.user_id = user
        new_review.prod_id = Product.objects.get(pk=p_id)
        new_review.review = review
        new_review.photo = photo
        new_review.save()
        return HttpResponseRedirect(reverse('shop:product_page', args=[slug]))
    return HttpResponseRedirect(reverse('shop:product_page', args=[slug]))


class Delivery(View):
    def get(self, request):
        return
        # return render(request, 'shop/delivery.html')


def success(request=None, param=None):
    print(param)
    if param is None:
        return HttpResponseRedirect(reverse('shop:index'))
    cookies = []
    return render(request, 'shop/success.html', {'param': param, 'cookies': json.dumps(cookies)})


@transaction.atomic
def charge(request):
    if request.method == 'POST':

        try:
            products = request.COOKIES['cart']  # trying get the cookie
            products = json.loads(products)
        except:
            return render(request, 'shop/cart.html')

        try:
            email = request.POST['email']
            phone = request.POST['phone']
            address = request.POST['address']
            comment = request.POST['comment']
            delivery = request.POST['delivery']
        except:
            text = ''
            return render(request, 'shop/error.html', {'text': text, 'img': 'oops.png'})

        order = Order()
        order.save()

        if request.user.is_authenticated:
            user = request.user
        elif not request.user.is_authenticated:
            try:
                user = User.objects.get(email=request.POST['email'])
            except:
                # generation link and user
                reg_link = AccUser()
                activation_link = AccUser.new_link(24)
                reg_link.acc_link = activation_link
                reg_link.save()
                # user
                user = User()
                user.is_active = False
                user.email = request.POST['email']
                user.username = request.POST['email']
                password = AccUser.new_link(8)
                user.set_password(password)
                user.save()
                reg_link.user = user
                reg_link.save()
                try:
                    send_mail(
                        'Your ',
                        f'Here is the your activation link:\nhttp://127.0.0.1:8000/acceptance_of_reg/{activation_link}.\n'
                        f'Login: use your email\nPassword: {password}',
                        from_email='noreply@ohgirls.eu',
                        recipient_list=[email],  # change email !!!!! =================
                        auth_user='vadym@ohgirls.eu',
                        auth_password='VadiM23071990*',  # encrypt password on server =================================
                        fail_silently=False,
                    )
                except Exception as es:
                    print(es)

        # validation cart objects
        price, weight = [], []
        try:
            with transaction.atomic():
                for i in products:
                    # get product
                    prod_id = int(i[0])
                    product = Product.objects.get(pk=prod_id)

                    # check is product draft or not
                    if product.draft == True:
                        text = f'Oops this item sold:\n{product.title}'
                        return render(request, 'shop/error.html', {'text': text, 'img': 'oops.png'})

                    # get quantity of product and change it
                    quant_prod = Sizes.objects.get(product=product)
                    quant_prod.quantity = F('quantity') - 1
                    quant_prod.save()
                    order_product = OrderProduct(user=user, order_id=order, product=product, size=quant_prod.size,
                                                 price=product.price)
                    order_product.save()
                    price.append(product.price)
                    weight.append(product.weight)
        except DatabaseError:
            order.delete()
            text = f'Oops some products was sold :(<br>' \
                   f'Product: {product.title}, we have only: {Sizes.objects.get(product=product).quantity}' \
                   f'<br> Please change quantity in your cart '
            return render(request, 'shop/error.html', {'text': text, 'img': 'oops.png'})
        except:
            return render(request, 'shop/cart.html')

        delivery_method = Deliveries.objects.get(pk=delivery)

        total_price = sum(price)+delivery_method.price
        total_weight = sum(weight)

        # save order detale
        order.address = address
        order.email = email
        order.phone = phone
        order.status = OrderStatus.objects.get(pk=1)
        order.user = user
        order.comment = comment
        order.price = total_price
        order.weight = total_weight
        order.delivery = delivery_method
        order.save()

        token = request.POST['stripeToken']
        stripe.Charge.create(
            amount=int(total_price*100),
            currency="eur",
            source=token,
            description=f"Order ID {order.id}"
        )
        order_id = order.id
        return success(param=order_id)


class Error(View):
    def get(self, request):
        return render(request, 'shop/error.html')
