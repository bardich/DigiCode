from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model."""
    phone = models.CharField(_('Phone Number'), max_length=20, blank=True)
    avatar = models.ImageField(_('Avatar'), upload_to='avatars/', blank=True)
    is_verified = models.BooleanField(_('Verified'), default=False)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
