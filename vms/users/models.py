# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, username, email, member_number, password=None, **extra_fields):
        if not member_number:
                raise ValueError('Users must have a member number')
        if not email:
                raise ValueError('Users must have an email address')
        if not password:
                raise ValueError('Users must have a password')

        user = self.model(
            member_number = member_number,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, member_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, member_number, password, **extra_fields)

    def create_superuser(self, username, email, member_number, password=None):
        if not member_number:
                raise ValueError('Users must have a member number')
        if not email:
                raise ValueError('Users must have an email address')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, member_number, password, **extra_fields)


@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    member_number = models.PositiveIntegerField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    REQUIRED_FIELDS = ['member_number', 'email']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
