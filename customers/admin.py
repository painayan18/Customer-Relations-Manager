from django.contrib import admin
from .models import Category, User, Customer, Agent, UserProfile

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(UserProfile)
