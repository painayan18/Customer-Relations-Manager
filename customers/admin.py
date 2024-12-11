from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.User)
admin.site.register(models.Customer)
admin.site.register(models.Agent)
admin.site.register(models.UserProfile)
