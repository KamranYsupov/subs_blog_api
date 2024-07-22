from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser, BaseUserManager

from .utils.hashers import hash_password, check_password
from django.core.validators import EmailValidator
from django.db import models

from .validators import password_validator


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserMixin(models.Model):
    objects = UserManager()
    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        'E-mail',
        unique=True,
        db_index=True,
        validators=[EmailValidator(message='Некорректный E-mail')]
    )
    password = models.CharField(
        'Пароль',
        max_length=20,
        validators=[password_validator]
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)
        self._password = raw_password

    def check_password(self, password):
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        super(UserMixin, self).save(*args, **kwargs)

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)


class User(UserMixin, PermissionsMixin):
    SUBSCRIBER = 'Подписчик'
    AUTHOR = 'Автор'
    ROLES = [
        ('subscriber', SUBSCRIBER),
        ('author', AUTHOR)
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='subscriber', db_index=True)


