

def get_url_by_user_role(user):
    # if vendor then sending to vendor dashboard
    if user.role == 1:
        return 'vendor_dashboard'
    
    # if cutomer then sending to cutomer dashboard
    elif user.role == 2:
        return 'customer_dashboard'
    
    # if anything else then sending to login page
    else:
        return 'login'