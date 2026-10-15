# ============================================================
# Global Messages
# Centralised field-keyed error and success messages for myapp.
#
# Error constants are plain dicts so you can pass them directly
# to Response() without any extra wrapping:
#
#   return Response(RegisterMessages.EMAIL_ALREADY_EXISTS,
#                   status=status.HTTP_400_BAD_REQUEST)
#
# -> {"email": "Email already exists."}
#
# Success constants are plain strings used under a "message" key:
#
#   return Response({"message": RegisterMessages.REGISTRATION_SUCCESSFUL},
#                   status=status.HTTP_201_CREATED)
# ============================================================


# ------------------------------------------------------------------
# AUTH - Registration
# ------------------------------------------------------------------
class RegisterMessages:
    # Field-level errors
    FULL_NAME_REQUIRED    = {"full_name": "Full name is required."}
    EMAIL_REQUIRED        = {"email": "Email is required."}
    PASSWORD_REQUIRED     = {"password": "Password is required."}
    ALL_FIELDS_REQUIRED   = {"non_field_errors": "All fields are required."}
    EMAIL_ALREADY_EXISTS  = {"email": "Email already exists."}

    # Success
    REGISTRATION_SUCCESSFUL = "Registration successful"


# ------------------------------------------------------------------
# AUTH - Login
# ------------------------------------------------------------------
class LoginMessages:
    # Field-level errors
    EMAIL_REQUIRED              = {"email": "Email is required."}
    PASSWORD_REQUIRED           = {"password": "Password is required."}
    ALL_FIELDS_REQUIRED         = {"non_field_errors": "Email and Password are required."}
    INVALID_EMAIL               = {"email": "No account found with this email."}
    INVALID_PASSWORD            = {"password": "Incorrect password."}
    INVALID_CREDENTIALS         = {"non_field_errors": "Invalid email or password."}

    # Success
    LOGIN_SUCCESSFUL = "Login Successful"


# ------------------------------------------------------------------
# AUTH - Logout
# ------------------------------------------------------------------
class LogoutMessages:
    # Field-level errors
    REFRESH_TOKEN_REQUIRED  = {"refresh": "Refresh token is required."}
    INVALID_REFRESH_TOKEN   = {"refresh": "Invalid or expired refresh token."}

    # Success
    LOGOUT_SUCCESSFUL = "Logout successful"


# ------------------------------------------------------------------
# AUTH - Token Refresh
# ------------------------------------------------------------------
class TokenMessages:
    # Field-level errors
    REFRESH_TOKEN_REQUIRED          = {"refresh": "Refresh token is required."}
    REFRESH_TOKEN_INVALID_OR_EXPIRED = {"refresh": "Refresh token is invalid or expired."}


# ------------------------------------------------------------------
# AUTH - Forgot Password
# ------------------------------------------------------------------
class ForgotPasswordMessages:
    # Field-level errors
    EMAIL_REQUIRED   = {"email": "Email is required."}
    USER_NOT_FOUND   = {"email": "No account found with this email."}
    OTP_SEND_FAILED  = "Failed to send OTP email: {error}"  # use .format(error=...) at call site

    # Success
    OTP_SENT_SUCCESSFULLY = "OTP sent successfully to your email."


# ------------------------------------------------------------------
# AUTH - Verify OTP
# ------------------------------------------------------------------
class VerifyOTPMessages:
    # Field-level errors
    EMAIL_REQUIRED          = {"email": "Email is required."}
    OTP_REQUIRED            = {"otp": "OTP is required."}
    ALL_FIELDS_REQUIRED     = {"non_field_errors": "Email and OTP are required."}
    USER_NOT_FOUND          = {"email": "No account found with this email."}
    INVALID_OR_EXPIRED_OTP  = {"otp": "Invalid or expired OTP."}

    # Success
    OTP_VERIFIED_SUCCESSFULLY = "OTP verified successfully."


# ------------------------------------------------------------------
# AUTH - Reset Password
# ------------------------------------------------------------------
class ResetPasswordMessages:
    # Field-level errors
    ALL_FIELDS_REQUIRED     = {"non_field_errors": "Email, OTP, new_password, and confirm_password are required."}
    PASSWORDS_DO_NOT_MATCH  = {"confirm_password": "New password and confirm password do not match."}
    USER_NOT_FOUND          = {"email": "No account found with this email."}
    INVALID_OR_EXPIRED_OTP  = {"otp": "Invalid or expired OTP."}

    # Success
    PASSWORD_RESET_SUCCESSFULLY = "Password reset successfully."


# ------------------------------------------------------------------
# AUTH - Change Password
# ------------------------------------------------------------------
class ChangePasswordMessages:
    # Field-level errors
    ALL_FIELDS_REQUIRED     = {"non_field_errors": "All fields are required."}
    OLD_PASSWORD_INCORRECT  = {"old_password": "Old password is incorrect."}
    PASSWORDS_DO_NOT_MATCH  = {"confirm_password": "New password and confirm password do not match."}

    # Success
    PASSWORD_CHANGED_SUCCESSFULLY = "Password changed successfully."


# ------------------------------------------------------------------
# DONATIONS
# ------------------------------------------------------------------
class DonationMessages:
    # Field-level errors
    IMAGE_REQUIRED              = {"image": "Image is required."}
    ONLY_UPDATE_OWN_DONATION    = {"detail": "You can only update your own donation."}
    ONLY_DELETE_OWN_DONATION    = {"detail": "You can only delete your own donation."}

    # Success
    DONATION_CREATED_SUCCESSFULLY = "Donation created successfully"
    DONATION_DELETED_SUCCESSFULLY = "Donation deleted successfully."


# ------------------------------------------------------------------
# LOCATION
# ------------------------------------------------------------------
class LocationMessages:
    # Field-level errors
    LATITUDE_REQUIRED   = {"latitude": "latitude query parameter is required."}
    LONGITUDE_REQUIRED  = {"longitude": "longitude query parameter is required."}
    LAT_LON_REQUIRED    = {"non_field_errors": "Both 'latitude' and 'longitude' query parameters are required."}
    INVALID_LATITUDE    = {"latitude": "Invalid numeric value for latitude."}
    INVALID_LONGITUDE   = {"longitude": "Invalid numeric value for longitude."}
    INVALID_RADIUS      = {"radius": "Invalid numeric value for radius."}
    INVALID_NUMERIC_VALUE = {"non_field_errors": "Invalid numeric value for latitude, longitude, or radius."}
