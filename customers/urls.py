from django.urls import path
from . import views as cv # customer views
urlpatterns = [
    path('', cv.CustomerListView.as_view(), name='customer-list'),
    path('create/', cv.CustomerCreateView.as_view(), name='customer-create'),
    path('<int:pk>/', cv.CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:pk>/update/', cv.CustomerUpdateView.as_view(), name='customer-update'),
    path('<int:pk>/delete/', cv.CustomerDeleteView.as_view(), name='customer-delete'),
    path('<int:pk>/assign-agent/', cv.AssignAgentView.as_view(), name='assign-agent'),
    path('categories/', cv.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', cv.CategoryDetailView.as_view(), name='category-details'),
]