from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import DesignRequest, Category

class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        label="ФИО",
        help_text="Только кириллица, пробелы и дефис"
    )
    username = forms.CharField(
        max_length=150,
        label="Логин",
        help_text="Только латиница и дефис"
    )
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Повтор пароля")
    consent = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True
    )

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', full_name):
            raise ValidationError("ФИО должно содержать только кириллицу, пробелы и дефис.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError("Логин должен содержать только латиницу и дефис.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return password_confirm


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Файл слишком большой. Максимум — 2 МБ.")
            if not photo.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise forms.ValidationError("Недопустимый формат файла. Разрешены: jpg, jpeg, png, bmp.")
        return photo