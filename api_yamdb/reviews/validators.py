"""reviews app custom validators."""
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_year(value):
    """Validate year field."""
    if value > datetime.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!'
        )
