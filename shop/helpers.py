from shop.models import My_Wishlist


def exist_wishlist(id,request):
    if My_Wishlist.objects.filter(user=request.user,product=id).exists():
        return True
    return False