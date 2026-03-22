from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class OTPPurpose(models.TextChoices):
    EMAIL_VERIFICATION = "email_verification", "Email Verification"
    EMAIL_LOGIN = "email_login", "Email Login"
    PASSWORD_RESET = "password_reset", "Password Reset"
    WHATSAPP_NUMBER_VERIFICATION = "phone_number_verification", "Phone Number Verification"
    WHATSAPP_LOGIN = "whatsapp_login", "WhatsApp Login"

class User(AbstractUser):
    
    username = None #    Remove the username field since we are using email as the unique identifier
    email = models.EmailField(max_length=255, unique=True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    secondary_phone_number = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    whatsapp_number_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' #Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['name'] #Make name a required field when creating a user
    
    objects = CustomUserManager() #Use the custom user manager for creating users and superusers

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # email index removed — unique=True already creates one automatically
            models.Index(fields=['whatsapp_number']),
        ]
        verbose_name ="User"
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class AddressType(models.TextChoices):
    HOME = 'home', 'Home'
    WORK = 'work', 'Work'
    OTHER = 'other', 'Other'


class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=AddressType.choices, default=AddressType.HOME)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # composite is better — queries always filter by user first, then is_default
            models.Index(fields=['user', 'is_default']),
        ]
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country}"

class UserOtp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    purpose = models.CharField(max_length=50, choices=OTPPurpose.choices)
    otp_hash = models.CharField(max_length=255)
    attempts_count = models.PositiveIntegerField(default=0)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['otp_hash']),
            models.Index(fields=['expires_at']),
            # typical OTP lookup: unused OTP for this user for this specific purpose
            models.Index(fields=['user', 'purpose', 'is_used']),
        ]
        verbose_name_plural = 'OTPs'
    
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} — {self.purpose} ({'used' if self.is_used else 'pending'})"