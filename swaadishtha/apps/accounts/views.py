from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .utils import generate_otp
from .models import User, UserOtp, OTPPurpose
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        print("User authentication result:", user)  # Debugging statement

        if user is not None:
            if not user.is_active:
                return render(
                    request,
                    'accounts/login.html',
                    {'error': 'Your account is inactive. Please contact support.'}
                )

            login(request, user)

            # Optional: store login IP
            user.last_login_ip = request.META.get("REMOTE_ADDR")
            user.save(update_fields=["last_login_ip"])

            return redirect('/')

        else:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Invalid email or password'}
            )

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/register.html",
                {
                    "error": "Email already registered",
                    "name": name, 
                    "email": email
                 }
            )

        user = User.objects.create(
            email=email,
            name=name,
            is_active=False
        )

        otp = generate_otp()

        UserOtp.objects.create(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            otp_hash=otp,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        print("OTP:", otp)  # For testing

        request.session["verify_user"] = str(user.user_id)

        return redirect("verify-email")

class VerifyEmailView(View):

    def get(self, request):
        return render(request, "accounts/verify_email.html")
    
    def post(self, request):

        otp = request.POST.get("otp")

        user_id = request.session.get("verify_user")

        if not user_id:
            return redirect("register")

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return redirect("register")

        otp_obj = UserOtp.objects.filter(
            user=user,
            purpose=OTPPurpose.EMAIL_VERIFICATION,
            is_used=False
        ).order_by("-created_at").first()

        if not otp_obj:
            return render(
                request,
                "accounts/verify_email.html",
                {"error": "Invalid verification request"}
            )

        # Check expiry
        if otp_obj.expires_at < timezone.now():
            return render(
                request,
                "accounts/register.html",
                {"error": "OTP has expired, please register again"}
            )

        # Check OTP match
        if otp_obj.otp_hash != otp:
            otp_obj.attempts_count += 1
            otp_obj.save(update_fields=["attempts_count"])

            return render(
                request,
                "accounts/verify_email.html",
                {"error": "Invalid OTP"}
            )

        # OTP valid
        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])

        user.email_verified = True
        user.save(update_fields=["email_verified"])

        # move to password step
        request.session["set_password_user"] = str(user.user_id)

        return redirect("set-password")

class SetPasswordView(View):
    def get(self,request):
        return render(request, "accounts/set_password.html")

    def post(self, request):
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        user_id = request.session.get("set_password_user")

        if not user_id:
            return redirect("register")

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return redirect("register")

        if password != confirm_password:
            return render(
                request,
                "accounts/set_password.html",
                {"error": "Passwords do not match"}
            )

        # Validate password strength
        try:
            validate_password(password, user)
        except ValidationError as e:
            return render(
                request,
                "accounts/set_password.html",
                {"error": e.messages[0]}
            )

        user.set_password(password)

        user.is_active = True

        user.save()

        login(request, user)

        del request.session["set_password_user"]

        return redirect("/")

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")