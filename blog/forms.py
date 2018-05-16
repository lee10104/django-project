from django import forms
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password',)

class PictureForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    link = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Picture
        exclude = ('category',)
