from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic
from agents.mixins import OrganiserAndLoginRequiredMixin
from .models import Customer, Category
from .forms import (
    CustomerModelForm, CustomUserCreationForm, AssignAgentForm,
    CategoryModelForm, CategoryUpdateForm
)

class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
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


class CustomerCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'customers/customer_create.html'
    form_class = CustomerModelForm

    def get_success_url(self):
        return reverse('customer-list')

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.organisation = self.request.user.userprofile
        customer.save()

        # TODO: send_mail(subject, message, from_email, recipient_list)
        # send_mail(
        #     subject="Customer Created",
        #     message=form.cleaned_data["Go to the site to view"],
        #     from_email="test@test.com",
        #     recipient_list=["test@test.com",],
        # )

        return super(CustomerCreateView, self).form_valid(form)


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


class CategoryCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'customers/category_create.html'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse('category-list')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


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


class CategoryUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'customers/category_update.html'
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse('category-list')

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


class CategoryDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "customers/category_delete.html"

    def get_success_url(self):
        return reverse('category-list')

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


class CustomerCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'customers/customer_category_update.html'
    form_class = CategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Customer.objects.filter(organisation=user.userprofile)
        else:
            queryset = Customer.objects.filter(organisation=user.agent.organisation)
            # filter for logged-in agent
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('customer-detail', kwargs={'pk': self.get_object().id})