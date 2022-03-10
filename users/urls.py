from django.urls import path
from users.views import SignupView, SigninView, ShoppingCartView

urlpatterns = [
    path('/signup',SignupView.as_view()),
    path('/signin',SigninView.as_view()),
    path('/shoppingcart',ShoppingCartView.as_view()),
]