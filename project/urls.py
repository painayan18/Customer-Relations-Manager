from django.contrib import admin
from django.urls import path, include
from customers.views import landing_page, LandingPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('customers/', include('customers.urls')),
]
