from django.urls import path

from . import views


urlpatterns = [
    path('user_registration/', views.user_registration, name='user_registration'),
    path('vendor_registration/', views.vendor_registration, name='vendor_registration'),
]