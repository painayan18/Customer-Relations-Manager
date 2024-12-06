from django.urls import path
from .views import customer_list, customer_detail, customer_create, customer_update

urlpatterns = [
    path('', customer_list, name='customer-list'),
    path('<int:pk>/', customer_detail, name='customer-detail'),
    path('<int:pk>/update/', customer_update, name='customer-update'),
    path('create/', customer_create, name='customer-create'),
]