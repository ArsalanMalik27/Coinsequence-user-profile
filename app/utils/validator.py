from contextlib import suppress

import phonenumbers
from email_validator import EmailNotValidError, validate_email


def get_validated_email(email_str: str) -> str | None:
    email = None
    with suppress(EmailNotValidError):
        email = validate_email(email_str, test_environment=True).email
    return email


def get_validated_phone(phone_str: str) -> str | None:
    phone = None
    with suppress(phonenumbers.phonenumberutil.NumberParseException):
        phonenumber = phonenumbers.parse(phone_str)
        if not phonenumbers.is_valid_number(phonenumber):
            return None
        phone = phonenumbers.format_number(
            phonenumber, phonenumbers.PhoneNumberFormat.E164
        )
    return phone
