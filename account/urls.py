from django.urls import path

from .views      import SignUpView, WishListView, ProfileImageView, SignInView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/profile', ProfileImageView.as_view()),
    path('/wishlist', WishListView.as_view()),
    path('/wishlist/<int:id>', WishListView.as_view()),  
]