from django.conf import settings


MFA_DEVICE_COOKIE_NAME = getattr(settings, "MFA_DEVICE_COOKIE_NAME", "remember_device_key")
MFA_DEVICE_MAX_AGE_DAYS = getattr(settings, "MFA_DEVICE_MAX_AGE", 180)
