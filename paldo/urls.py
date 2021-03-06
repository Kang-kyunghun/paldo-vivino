from django.urls import path, include

urlpatterns = [
    path('products', include('product.urls')),
    path('accounts', include('account.urls')),
    path('orders', include('order.urls')),
]
