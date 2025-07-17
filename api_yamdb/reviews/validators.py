"""reviews app custom validators."""
from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """Validate year field."""
    if value > datetime.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!'
        )
