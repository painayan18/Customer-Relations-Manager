from django import forms
from customers.models import Agent

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = (
            'user',
        )