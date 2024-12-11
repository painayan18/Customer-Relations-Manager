from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganiserAndLoginRequiredMixin
from .models import Customer, Agent, User, Category
from .forms import (
    CustomerForm,
    CustomerModelForm,
    CustomUserCreationForm,
    AssignAgentForm,
)

class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class CustomerListView(LoginRequiredMixin, generic.ListView):
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

    # initial queryset
    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False,
            )
        else:
            queryset = Customer.objects.filter(
                organisation=user.agent.organisation,
                agent_isnull=False,
            )
            # filter for logged-in agent
            queryset = queryset.filter(agent__user=user)

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CustomerListView, self).get_context_data(**kwargs)

        if user.is_organiser:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                'unassigned_customers': queryset
            })

        return context


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
    template_name = 'customers/customer_create.html'
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse('customer-list')

    def form_valid(self, form):

        # TODO: send_mail(subject, message, from_email, recipient_list)

        return super(CustomerCreateView, self).form_valid(form)


class CustomerUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'customers/customer_update.html'
    form_class = CustomerModelForm

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('customer-list')


class CustomerDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'customers/customer_delete.html'

    def get_success_url(self):
        return reverse('customer-list')

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.filter(organisation=user.userprofile)


class AssignAgentView(OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = 'customers/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def get_success_url(self):
        return reverse('customer-list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        customer = Customer.objects.get(id=self.kwargs['pk'])
        customer.agent = agent
        customer.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'customers/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)

        if user.is_organiser:
            queryset = Customer.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Customer.objects.filter(
                organisation=user.agent.organisation,
            )

        context.update({
            'unassigned_customer_count': queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation,
            )

        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'customers/category_detail.html'
    context_object_name = 'category'

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     customers = self.get_object().customers.all()
    #     context.update({
    #         'customers': customers
    #     })
    #
    #     return context

    def get_queryset(self):
        user = self.request.user

        if user.is_organiser:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation,
            )

        return queryset