from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.views import View

class OrganiserAndLoginRequiredMixin(AccessMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
            return redirect("customer-list")
        return super().dispatch(request, *args, **kwargs)