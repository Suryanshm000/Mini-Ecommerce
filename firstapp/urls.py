from django.urls import path
from . import views

app_name = 'firstapp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:pk>/', views.remove_cart, name='remove_cart'),
    path('cart/', views.cart, name='cart'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/add_product/', views.add_product, name='add_product'),
    path('vendor/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('vendor/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]