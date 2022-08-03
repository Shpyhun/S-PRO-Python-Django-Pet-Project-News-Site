from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", null=True)
    email = models.EmailField()

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_id': self.pk})

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

