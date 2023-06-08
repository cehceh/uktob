from django.core.validators import RegexValidator
from django.db import models
import os
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    # USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username',]


    def __str__(self):
        return '{}'.format(self.username)

    class Meta:
        app_label = "authentication"
        verbose_name = "custom_user"
        verbose_name_plural = "CustomUsers"
        indexes = [
            models.Index(
                fields=[
                    # "phone_number",
                    # "country_code",
                    # "gender",
                    # "email",
                    # "status",
                ]
            )
        ]
