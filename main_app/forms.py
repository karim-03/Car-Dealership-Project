from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Cars, Requests

class CustomUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False, label='Sign up as admin')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", 'is_admin')

    def save(self, commit=True):
        user = super().save(commit=False)
        is_admin = self.cleaned_data.get('is_admin')
        user.role = 'Admin' if is_admin else 'Customer'
        if commit:
            user.save()
        return user

class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ["brand", "model", "year", "price"]