from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'

    # Add a token field to your CustomUser model
    token = models.CharField(max_length=255, blank=True, null=True)

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def save(self, *args, **kwargs):
        # Generate a token when saving the user (you can customize this logic)
        if not self.token:
            self.token = generate_token()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


def generate_token():
    # Implement your token generation logic here (e.g., using secrets module)
    pass


class Configuration(models.Model):
    """ This is a model for bot configurations """
    panel_username = models.CharField(max_length=255, default=None)
    panel_password = models.CharField(max_length=255, default=None)
    bot_name = models.CharField(max_length=255)
    panel_url = models.CharField(max_length=255, blank=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.bot_name


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TelegramChannel(models.Model):
    """ This is a model for user telegram channels """
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    """ This is a model for handling the tutorials of bot """
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=2043, default=None)

    def __str__(self):
        return self.name


class ChannelAdmin(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.subject
