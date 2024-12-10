from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganiserAndLoginRequiredMixin
from .models import Customer, Agent
from .forms import CustomerModelForm, CustomUserCreationForm

class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class CustomerListView(LoginRequiredMixin, generic.ListView):
    template_name = "customers/customer_list.html"
    queryset = Customer.objects.all()
    context_object_name = 'customers'


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "customers/customer_detail.html"
    queryset = Customer.objects.all()
    context_object_name = 'customer'


class CustomerCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "customers/customer_create.html"
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse("customer-list")


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "customers/customer_update.html"
    queryset = Customer.objects.all()
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse("customer-list")


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "customers/customer_delete.html"
    queryset = Customer.objects.all()

    def get_success_url(self):
        return reverse("customer-list")
