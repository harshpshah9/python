from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.list  import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
class BaseListView(ListView):
    pass
class BaseTemplateView(TemplateView):
    pass

class BaseUpdateView(UpdateView):
    pass

class BaseDeleteView(DeleteView):
    pass
class BaseCreateView(CreateView):
    pass
class BaseLoginView(LoginView):
    pass

class BaseDetailView(DetailView): 
    pass

class BaseRedirectView(RedirectView):
    pass