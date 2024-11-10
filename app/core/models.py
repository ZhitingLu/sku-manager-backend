"""
Database models
"""
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """ Manager for the user model """

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # # Hash and set the password
        user.save(using=self._db)  # Save the user in the database

        return user

    def normalize_email(self, email):
        """ Normalize the email address by making it lowercase. """
        return email.lower()

    def create_superuser(self, email, password):
        """ Creates and saves a new superuser """
        user = self.model(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()  # custom manager for handling User model queries

    USERNAME_FIELD = 'email'


class MedicationSKU(models.Model):
    """
    Medication SKU Object

    A MedicationSKU is unique by:
    1. Global uniqueness of the `medication_name`.
    2. A unique combination of:

     - `medication_name`,
     - `presentation`,
     - `dose`,
     - and `unit`.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    medication_name = models.CharField(max_length=255, unique=True)
    presentation = models.CharField(max_length=255)
    dose = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = (
            (
                'medication_name',
                'presentation',
                'dose',
                'unit'
            ),
        )
        verbose_name = 'Medication SKU'
        verbose_name_plural = 'Medication SKUs'

    def __str__(self):
        return self.medication_name
