from django.urls import path, include
from . import views


app_name = 'shop'
urlpatterns = [ path('',views.Index.as_view(), name='index'),
                path('category/<slug:slug>/',views.CategoryPage.as_view(), name='category_page'),
                path('acceptance_of_reg/<str:slug>/', views.AccReg.as_view(), name='acc_reg'),
                path('account/', views.account, name='account'),
                path('login/', views.LoginPage.as_view(), name ='login'),
                path('curt/',views.CartPage.as_view(), name='cart'),
                path('reg_new_account/',views.RegAccountPage.as_view(), name='registration'),
                path('change_data/',views.change_data, name='change_data'),
                path('add_review/',views.add_review, name='add_review'),
                path('delivery/',views.Delivery.as_view(), name='delivery'),
                path('checkout/',views.CheckoutPage.as_view(), name='checkout'),
                path('error/',views.Error.as_view(), name='error'),
                path('success/',views.success, name='success'),
                path('charge/',views.charge, name='charge'),
                path('accaddress/', views.AccAddress.as_view(), name='acc_address'),



                path('<str:slug>/', views.ProductPage.as_view(), name='product_page'),
            ]