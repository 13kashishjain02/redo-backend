from shop.models import My_Wishlist,Cart


def exist_wishlist(id,request):
    if My_Wishlist.objects.filter(user=request.user,product=id).exists():
        return True
    return False

def Total_MRP(request):
    products = Cart.objects.filter(user=request.user,product_variation=None)
    products_v = Cart.objects.filter(user=request.user,product=None)
    total_mrp = []
    for mrp in products:
        total_mrp.append(mrp.product.special_price*mrp.quantity)
    for mrp in products_v:
        total_mrp.append(mrp.product_variation.special_price*mrp.quantity)
    return sum(total_mrp)

        