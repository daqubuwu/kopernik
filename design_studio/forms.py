from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

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
            'experience': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Опишите ваш опыт работы в дизайне...'
            }),
            'portfolio_link': forms.URLInput(attrs={
                'placeholder': 'https://ваше-портфолио.example.com'
            }),
        }
        labels = {
            'portfolio_link': 'Ссылка на портфолио',
            'specialization': 'Специализация',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Добавляем поле статуса только для администраторов
        if self.user and self.user.is_superuser:
            self.fields['status'] = forms.ChoiceField(
                choices=DesignerApplication.STATUS_CHOICES,
                label='Статус заявки',
                initial='new'
            )

            # Переупорядочиваем поля, если нужно
            field_order = list(self.fields.keys())
            field_order.insert(3, 'status')
            self.order_fields(field_order)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class NewStageForm(forms.ModelForm):
    class Meta:
        model = WorkStage
        fields = ['title', 'description']