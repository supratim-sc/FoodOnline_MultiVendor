from django.urls import path

from accounts import views as accounts_views
from . import views

urlpatterns = [
    path('', accounts_views.vendor_dashboard, name='vendor_dashboard'),
    path('my-restaurant/', views.my_restaurant, name='my_restaurant'),
]