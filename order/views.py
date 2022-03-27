from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from base.permission import SuperuserAccessMixin
from user.models import UserAddress
from .models import Order,OrderItem
from cart.models import Cart
from base.views import  BaseDetailView, BaseListView,BaseRedirectView, BaseUpdateView

# Create your views here.
class PlaceorderView(LoginRequiredMixin,BaseRedirectView):
    def get(self, request):
        user=self.request.user
        cart_item=Cart.objects.filter(user=user)
        address=self.request.GET.get('custid')
        add=UserAddress.objects.get(id=address)
        order=Order.objects.create(user=user,address=add)
        order.save()
        total_amount = 0 
        for cart in cart_item:
            qty=cart.qty
            product = cart.product    
            amount=cart.product.price * cart.qty
            total_amount += amount 
            OrderItem.objects.create(order=order,product=product,qty=qty,price=amount) 
            cart.delete() 
            print(total_amount)
        # print(order)

        order.total_amount = total_amount
        # # order.total_amount.save() 
        order.save()      
        return render(request, 'userportal/confirmation.html')

class OrderListView(LoginRequiredMixin,BaseListView):
    template_name='userportal/orderlist.html'
    model=Order
    context_object_name='orders'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class AdminOrderListView(SuperuserAccessMixin,BaseListView):
    template_name='adminportal/orderlist.html'
    model=Order
    context_object_name='orders'


class AdminOrderDetailView(SuperuserAccessMixin,BaseDetailView):
    template_name='adminportal/orderdetails.html'
    model=Order
    context_object_name='orders'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.kwargs.get('pk')
        context['orderitem'] = OrderItem.objects.filter(order=order)
        return context
class OrderStatusUpdateView(BaseUpdateView):
    model=OrderItem
    template_name='adminportal/orderstatusupdate.html'
    fields=['status']
    success_url=reverse_lazy('order:order_admin_list')

    
class OrderDetailView(LoginRequiredMixin,BaseDetailView):
    template_name = 'userportal/orderdetail.html'
    model= Order
    context_object_name='order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.kwargs.get('pk')
        # print(order)
        context['orderitem'] = OrderItem.objects.filter(order=order)
        # print(context)
        return context

