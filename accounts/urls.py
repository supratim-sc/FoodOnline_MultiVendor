from django.urls import path

from . import views


urlpatterns = [
    path('user_registration/', views.user_registration, name='user_registration'),
    path('vendor_registration/', views.vendor_registration, name='vendor_registration'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('my_account/', views.my_account, name='my_account'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('vendor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),

    path('account_activation/<user_id_encoded>/<token>', views.account_activation, name='account_activation'),

    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password_validation/<user_id_encoded>/<token>', views.reset_password_validation, name='reset_password_validation'),


]