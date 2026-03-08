import secrets
import string

def generate_otp(length: int = 6) -> str:
    """
    Generate a cryptographically secure numeric OTP.

    Args:
        length (int): Length of the OTP. Must be > 0.

    Returns:
        str: Secure randomly generated OTP.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("OTP length must be a positive integer.")

    digits = string.digits  # '0123456789'
    return ''.join(secrets.choice(digits) for _ in range(length))
