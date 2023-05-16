from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        # Creates a new user profile.

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)  # create a new user instance

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password, **extra_fields):
        # Creates and saves a new superuser with given details.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, name, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    # Represents a "user profile" inside out system. Stores all user account
    # related data, such as 'email address' and 'name'.

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()  # assign to the default manager attribute

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # Django uses this when it needs to get the user's full name.

        return self.name

    def get_short_name(self):
        # Django uses this when it needs to get the users abbreviated name.

        return self.name

    def __str__(self):
        # Django uses this when it needs to convert the object to text.

        return self.email
