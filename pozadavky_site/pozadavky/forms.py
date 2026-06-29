# coding: utf-8
from django import forms

from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
#     info = forms.CharField(label='Informace', widget=forms.Textarea, required=False)
    password1 = forms.CharField(label='Heslo', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Heslo znovu', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        if self.cleaned_data.get('password1') != self.cleaned_data['password2']:
            raise forms.ValidationError('Zadaná hesla se liší.')

        return self.cleaned_data['password2']