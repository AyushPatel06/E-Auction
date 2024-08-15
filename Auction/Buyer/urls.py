from django.urls import path
from . import views

app_name = 'Buyer'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_signup, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about-us/', views.about, name='about-us'),
    path('MenuFilter/<str:querys>', views.MenuFilter, name="MenuFilter"),
    path('search/', views.search, name="search"),
    path("product/<int:prod_id>", views.productView, name="ProductView"),
    path('contact/', views.contact, name="contact"),
    path('checkout/<int:prod_id>', views.checkout, name="checkout"),
    path('profile/', views.Profile, name="profile"),
    path('myorders/', views.MyOrders, name="myorders"),
    path('en-us/response/', views.response, name='response'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('FAQ/', views.faq, name='faq'),
    ]