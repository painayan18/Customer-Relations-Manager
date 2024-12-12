from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from customers.models import Customer, User, Agent, Category


# User = get_user_model()

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'first_name',
            'last_name',
            'agent',
            'description',
            'phone_number',
            'email',
        )


class CustomerForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'category',
        )