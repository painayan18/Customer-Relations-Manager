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
    context_object_name = "customers"

    # initial queryset
    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Customer.objects.filter(organisation=user.userprofile)
        else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation)
            # filter for logged-in agent
            queryset = queryset.filter(agent__user=user)

        return queryset



class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "customers/customer_detail.html"
    context_object_name = 'customer'

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Customer.objects.filter(organisation=user.userprofile)
        else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation)
            # filter for logged-in agent
            queryset = queryset.filter(agent__user=user)

        return queryset


class CustomerCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "customers/customer_create.html"
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse("customer-list")

    def form_valid(self, form):
        # send_mail() with parameters subject, message, from_email, recipient_list
        return super(CustomerCreateView, self).form_valid(form)

class CustomerUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "customers/customer_update.html"
    form_class = CustomerModelForm

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("customer-list")


class CustomerDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "customers/customer_delete.html"

    def get_success_url(self):
        return reverse("customer-list")

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(organisation=user.userprofile)