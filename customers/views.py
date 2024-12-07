from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from .models import Customer, Agent
from .forms import CustomerModelForm

class RegisterView(generic.CreateView):
    template_name = "auth/register.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login')
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

class CustomerListView(generic.ListView):
    template_name = "customers/customer_list.html"
    queryset = Customer.objects.all()
    context_object_name = 'customers'

class CustomerDetailView(generic.ListView):
    template_name = "customers/customer_detail.html"
    queryset = Customer.objects.all()
    context_object_name = 'customer'

class CustomerCreateView(generic.CreateView):
    template_name = "customers/customer_create.html"
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse("customer-list")

class CustomerUpdateView(generic.UpdateView):
    template_name = "customers/customer_update.html"
    queryset = Customer.objects.all()
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse("customer-list")

class CustomerDeleteView(generic.DeleteView):
    template_name = "customers/customer_delete.html"
    queryset = Customer.objects.all()

    def get_success_url(self):
        return reverse("customer-list")
