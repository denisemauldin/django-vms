# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import logging
log = logging.getLogger(__name__)


class SignupForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'name',
                  'member_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            self._meta.model.objects.get(email=email)
        except self._meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self._meta.model.objects.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    # handled by the adapter
    def save(self, user):
        log.info("SignupForm saving user ")
        return user

class MyAdminChangeForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('name', 'member_number', )

    def save(self, commit=True):
        log.info("MyAdminChageform saving user ")
        user = super(MyAdminChangeForm, self).save(commit=False)
        if user.pk:
            orig_user = self._meta.model.objects.get(pk=user.pk)
            if user.password != orig_user.password:
                user.set_password(self.cleaned_data["password"])
        else:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
