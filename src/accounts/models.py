from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AbstractUserManager
from django.db import models


class UserManager(AbstractUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    class UserRole(models.TextChoices):
        OWNER = "OW", "Owner"
        CUSTOMER = "CU", "Customer"

    role = models.CharField(
        max_length=2,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_customer(self):
        return self.role == User.UserRole.CUSTOMER

    def is_complete(self):
        if not self.first_name or not self.last_name or not self.phone_number:
            return False
        return True


class Information(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info")
    address = models.CharField(max_length=150, blank=True, null=True)
    address_2 = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=5, blank=True, null=True)
    district = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email
