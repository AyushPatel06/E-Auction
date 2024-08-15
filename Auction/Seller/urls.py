from django.urls import path
from . import views

app_name = 'Seller'
urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('chart/filter-options/', views.get_filter_options, name='chart-filter-options'),
    path('chart/sales/<int:year>/', views.get_sales_chart, name='chart-sales'),
    path('add-product/', views.add_product, name='add_product'),
    path('my-product/', views.view_product, name='my_product'),
    path('edit-product/<int:prod_id>',views.editproduct, name='edit_product'),
    path('myorders/',views.myorders,name='myorders'),
    path('search/',views.search,name='search'),
    path('profile/',views.profile,name='profile'),
    ]
