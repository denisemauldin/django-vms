# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import MyAdminChangeForm, SignupForm
from .models import User

class MyUserAdmin(AuthUserAdmin):

    form = MyAdminChangeForm
    fieldsets = (
            (None, {'fields': ('email', 'password')}),
            (_('User Profile'), {'fields': ('name', 'member_number')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                                       'groups', 'user_permissions')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ) #+ AuthUserAdmin.fieldsets

    # I don't know why SignupForm doesn't work here, but it throws a commit error
    # save() got an unexpected keyword argument 'commit'
    add_form = MyAdminChangeForm
    add_fieldsets = (
                        (None, {
                                'classes': ('wide',),
                                'fields': ('username', 'email', 'member_number', 'password')}
                        ),
                    )
    list_display = ('username', 'name', 'member_number', 'is_superuser', 'is_staff')
    search_fields = ['name', 'member_number']

admin.site.register(User, MyUserAdmin)
