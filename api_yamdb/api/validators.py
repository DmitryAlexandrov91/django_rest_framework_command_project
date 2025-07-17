"""api app custom validators."""
import re

from django.core.exceptions import ValidationError

from .constants import USERNAME_PATTERN


def validate_restricted_symbols(value):
    """Validate for restricted symbols in username."""
    if not USERNAME_PATTERN.fullmatch(value):
        restricted_symbols = re.findall(r'\W', value)
        raise ValidationError('В имени пользователя есть запрещенные символы '
                              f'{restricted_symbols}')
