from django.utils.translation import ugettext as _

from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

from .models import AdvUser

from captcha.fields import CaptchaField


class ChangedUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('photo', 'username', 'email', 'first_name', 'last_name', 'description')

#
# class RegisterUserForm(forms.ModelForm):
#     email = forms.EmailField(required=True, label='Адрес электронной почты')
#     password1 = forms.CharField(label='Пароль',
#                                 widget=forms.PasswordInput,
#                                 help_text=password_validation.password_validators_help_text_html())
#     password2 = forms.CharField(label='Пароль повторно',
#                                 widget=forms.PasswordInput,
#                                 help_text='Введите тот же самый пароль ещё раз для проверки')
#     captcha = CaptchaField(label='Введите текст с картинки ', error_messages={'invalid': 'Неправильный текст'}, generator='captcha.helpers.math_challenge')
#
#     def clean_password1(self):
#         password1 = self.cleaned_data['password1']
#         if password1:
#             password_validation.validate_password(password1)
#         return password1
#
#     def clean(self):
#         super(RegisterUserForm, self).clean()
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']
#         if password1 and password2 and password1 != password2:
#             errors = {'password2': ValidationError(
#                 'Введённые пароли не совпадают', code='password_mismatch')}
#             raise ValidationError(errors)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user
#
#     class Meta:
#         model = AdvUser
#         fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'photo', 'description', 'captcha')
#


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    # check = forms.BooleanField(label=lazy(lambda: _("Privacy <a href='%s' a>policy</a>" % reverse('users:privacy'))))
    # check = forms.BooleanField(required=True, label=mark_safe("I accept the terms and <a href='{%s}'>conditions.</a>" % reverse_lazy('users:privacy')))
    check = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['check'].label = mark_safe('Принимаю <a target="_blank" href=%s> политику конфиденциальности</a>' % reverse_lazy('users:privacy'))

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'check')