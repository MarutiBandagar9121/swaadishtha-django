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
    EMAIL_VERIFICATION = "email_verification", "Email_Verification"
    EMAIL_LOGIN = "email_login", "Email_Login"
    PASSWORD_RESET = "password_reset", "Password_Reset"
    WHATSAPP_NUMBER_VERIFICATION = "phone_number_verification", "Phone_Number_Verification"
    WHATSAPP_LOGIN = "whatsapp_login", "WhatsApp_Login"

class User(AbstractUser):
    
    username = None #    Remove the username field since we are using email as the unique identifier
    email = models.EmailField(max_length=255, unique=True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    secondary_phone_number = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    whatsapp_number_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email' #Set email as the unique identifier for authentication
    REQUIRED_FIELDS = ['name'] #Make name a required field when creating a user
    
    objects = CustomUserManager() #Use the custom user manager for creating users and superusers

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['whatsapp_number']),
        ]
        verbose_name ="User"
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.name} ({self.email}), user_id: {self.user_id}"

class UserOtp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    purpose = models.CharField(max_length=50, choices=OTPPurpose.choices)
    otp_hash = models.CharField(max_length=255)
    attempts_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['otp_hash']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['user','is_used']),
        ]
        verbose_name_plural = 'OTPs'
    
    def is_expired(self):
        return timezone.now() > self.expires_at