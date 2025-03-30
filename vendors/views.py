from django.shortcuts import render

# Create your views here.
def my_restaurant(request):
    return render(request, 'accounts/vendor_my_restaurant.html')