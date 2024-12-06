from django import forms
from customers.models import Customer

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )

class CustomerForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)