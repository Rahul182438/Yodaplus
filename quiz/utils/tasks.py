import pyotp



def generate_otp():
    """
    A  OTP generate function.
    OTP generated with PyOTP library with the current timestamp
    """
    totp = pyotp.TOTP('base32secret3232')
    generate_otp  = totp.now()

    return generate_otp