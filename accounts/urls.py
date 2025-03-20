from django.urls import path

from . import views


urlpatterns = [
    path('user_registration/', views.user_registration, name='user_registration'),
    path('vendor_registration/', views.vendor_registration, name='vendor_registration'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]