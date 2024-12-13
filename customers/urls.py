from django.urls import path
from .views import (
    CustomerListView, CustomerCreateView, CustomerDetailView,
    CustomerUpdateView, CustomerDeleteView, AssignAgentView,
    CategoryListView, CategoryCreateView, CategoryDetailView,
    CategoryUpdateView, CategoryDeleteView, CustomerCategoryUpdateView
)

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),
    path('create/', CustomerCreateView.as_view(), name='customer-create'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-details'),
    path('<int:pk>/category/', CustomerCategoryUpdateView.as_view(), name='customer-category-update'),



]
