from .models import Vendor

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except (Vendor.DoesNotExist, ValueError, TypeError):
        vendor = None
    return dict(vendor=vendor)