from django.urls import path
from users.views import SignupView, SigninView, WishlistView
 

urlpatterns = [
    path('/signup',SignupView.as_view()),
    path('/signin',SigninView.as_view()),
    path('/wishlist',WishlistView.as_view()),
    #path('/wishlist/<int:product_id>',WishlistView.as_view())
    
]