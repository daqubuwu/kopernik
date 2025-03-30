from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import ClientRequest, DesignerApplication

class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ['name', 'email', 'phone', 'project_type', 'description', 'budget']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class DesignerApplicationForm(forms.ModelForm):
    class Meta:
        model = DesignerApplication
        fields = ['name', 'email', 'phone', 'portfolio_link', 'experience', 'specialization']
        widgets = {
            'experience': forms.Textarea(attrs={'rows': 4}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))