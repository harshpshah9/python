from cart.models import Cart
def tot_amount(user):
    grand_total = 0
    amount = 0
    cart_item=Cart.objects.filter(user=user)
    for cart in cart_item:
        amount=cart.product.price * cart.qty
        grand_total += amount
    return grand_total