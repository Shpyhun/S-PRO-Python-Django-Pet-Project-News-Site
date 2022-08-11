from allauth.account.models import EmailAddress
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password is not provided')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        null=True,
        blank=True,
        max_length=150,
    )
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}"

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_username(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['email', ]

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.pk})


