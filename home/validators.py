import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# class CustomPasswordValidator:
def validate_password_strength(password):
        if len(password) < 8 or len(password) > 20:
            raise ValidationError(
                _("Password must be between 8 and 20 characters long."),
                code='password_length',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one Captial(uppercase) letter."),
                code='password_no_letter',
            )

        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least one Captial(uppercase) letter."),
                code='password_no_letter',
            )

        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )

        if not re.search(r'[\W_]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

        if re.search(r'\s', password):
            raise ValidationError(
                _("Password must not contain spaces."),
                code='password_space',
            )

        if re.search(r'[\U0001F600-\U0001F64F]', password):
            raise ValidationError(
                _("Password must not contain emojis."),
                code='password_emoji',
            )

    # def get_help_text(self):
    #     return _(
    #         "Your password must be 8-20 characters long, contain letters, numbers, and special characters, "
    #         "and must not contain spaces or emojis."
    #     )
