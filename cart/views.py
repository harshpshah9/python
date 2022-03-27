
# Create your views here.
from django.shortcuts import render,redirect
from django.views.generic import View
from base.views import BaseCreateView, BaseDeleteView, BaseListView,BaseUpdateView,BaseTemplateView
from cart.utils import tot_amount
from cart.models import Cart
from product.models import Product
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import UserAddress
# Create your views here.

class AddToCart(LoginRequiredMixin,View):
    template_name='userportal/index.html'
    def post(self,request, *args, **kwargs):
        product_id=self.kwargs.get('productid')
        product=Product.objects.get(id=product_id)    
        qty =request.POST.get('qty')
        try:
            if qty:
                qty = eval(qty)
                cart, is_created = Cart.objects.get_or_create(user=self.request.user, product=product)
                if is_created:
                    cart.qty = qty
                else:
                    cart.qty += qty
                cart.save()
            else:
                Cart.objects.create(user=self.request.user, product=product)
            # messages.success(request, 'Add to cart successfully!')    
            
        except Exception:
            return HttpResponse("Exception: Data not found") 
        return JsonResponse(data={
                'message' : 'cart created successfully'
            })
class CartDeleteView(LoginRequiredMixin,View):
    model=Cart
    success_url=reverse_lazy('cart:list')
    
    def post(self, request, *args, **kwargs):        
        cart_id = kwargs.get("cart_item_id")
        try:
            cart=Cart.objects.get(id=cart_id)
            cart.delete()
            user=self.request.user
            grand_total = tot_amount(user) 
        except Exception:
             return HttpResponse("Exception: Data not found")  
        return JsonResponse(data={
                'message' : 'cart deleted successfully','grand_total':grand_total
            })

class CartQtyChangeView(LoginRequiredMixin,View):
    def post(self, request ,*args, **kwargs):
        product_id=request.POST.get('product_id')
        print(product_id)
        update_qty =request.POST.get('update_qty')
        print(update_qty)
        
        qty = eval(update_qty)
        print(type(qty))
        product=Product.objects.get(id=product_id) 
        cart=Cart.objects.get(user=self.request.user, product=product)
        cart.qty=qty
        cart.save()
        amount=cart.qty*product.price
        user=self.request.user
        grand_total = tot_amount(user) 
        return JsonResponse(data={'message' : 'cart  updated successfully','amount':amount,'grand_total':grand_total})

class CartListView(LoginRequiredMixin,BaseListView):
    template_name='userportal/cart.html'
    model=Cart
    def get(self,request):
        user=self.request.user
        cart_item=Cart.objects.filter(user=user)
        grand_total = tot_amount(user) 
        print('grand total',grand_total)
        return render(request,'userportal/cart.html',{'carts':cart_item,'grand_total':grand_total})
         

class CheckoutCart(BaseTemplateView):
    template_name='userportal/checkout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart']= Cart.objects.filter(user=self.request.user) 
        context['user_addresses']=UserAddress.objects.filter(user=self.request.user)
        context['total'] =  tot_amount(user=self.request.user) 
        return context