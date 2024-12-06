from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Customer, Agent
from .forms import CustomerForm, CustomerModelForm

def customer_list(request):
    customers = Customer.objects.all()
    context = {
        "customers" : customers
    }
    return render(request, 'customers/customer_list.html', context)

def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    context = {
        "customer": customer
    }
    return render(request, "customers/customer_detail.html", context)

def customer_create(request):
    form = CustomerModelForm()
    if request.method == "POST":
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-list')

    context = {
        "form": form
    }
    return render(request, "customers/customer_create.html", context)

def customer_update(request, pk):
    customer = Customer.objects.get(pk=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == "POST":
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-detail', pk=customer.pk)

    context = {
        "form": form,
        "customer": customer
    }
    return render(request, 'customers/customer_update.html', context)

def customer_delete(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.delete()
    return redirect('customer-list')

# def customer_update(request, pk):
#     customer = Customer.objects.get(pk=pk)
#     form = CustomerForm()
#     if request.method == "POST":
#         print("receiving a POST request")
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             customer.first_name = first_name
#             customer.last_name = last_name
#             customer.age = age
#             customer.save()
#             return redirect('customer-list')
#
#     context = {
#         "form": CustomerForm()
#     }
#     context = {
#         "customer": customer
#     }
#     customer = Customer.objects.get(pk=pk)
#     return render(request, 'customers/customer_update.html', context)

# def customer_create(request):
#     form = CustomerModelForm()
#     if request.method == "POST":
#         print("receiving a POST request")
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             print("form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Customer.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             return redirect('customer-list')
#
#     context = {
#         "form": CustomerModelForm()
#     }
#     return render(request, "customers/customer_create.html", context)
