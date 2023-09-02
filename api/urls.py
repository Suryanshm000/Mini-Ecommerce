from django.urls import path
from . import views
# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('get_products/', views.get_products, name='get_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
]
