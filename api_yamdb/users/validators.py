"""user app custom validators."""
from django.core.exceptions import ValidationError
from api.constants import RESTRICTED_NAMES


def validate_username(value):
    """Validate username field."""
    if value in RESTRICTED_NAMES:
        raise ValidationError(f'Нельзя использовать имя {value}!')
