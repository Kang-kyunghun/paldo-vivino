from django.urls import path

from .views      import CartsView

urlpatterns = [
    path('/carts', CartsView.as_view()),
    path('/carts/<int:id>', CartsView.as_view()),
]
