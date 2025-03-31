from django.shortcuts import render

# Create your views here.
def my_restaurant(request):
    return render(request, 'vendors/vendor_my_restaurant.html')