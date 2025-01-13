from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'avatar']

    first_name = forms.CharField(
        label='Имя', max_length=30)
    avatar = forms.ImageField(label='Поменять аватар')
