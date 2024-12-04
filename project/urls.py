from django.contrib import admin
from django.urls import path
from customers.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
]
