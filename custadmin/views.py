from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class AdminDashboard(TemplateView):
    template_name='adminportol/dashboard.html'