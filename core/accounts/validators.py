from django.core.validators import RegexValidator


iranian_phone_number_validator = RegexValidator(
    regex=r'^(?:\+98|0)?9\d{9}$',
    message="Phone number must be entered in the format: '+989123456789' or '09123456789'."
)