from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
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

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        null=True,
        blank=True,
        max_length=150,
    )
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    email_verify = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"{self.pk}"

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ['id', 'email']

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.pk})


# class Profile(models.Model):
#     slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", null=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.user
#
#     def get_absolute_url(self):
#         return reverse('profile', kwargs={'profile_id': self.pk})
#
#     class Meta:
#         verbose_name = 'Profile'
#         verbose_name_plural = 'Profiles'
#         ordering = ['id', 'user']
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

