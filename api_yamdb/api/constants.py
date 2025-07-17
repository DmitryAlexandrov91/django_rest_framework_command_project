"""api_yamdb project constants."""
import re

CUT_OFF_MAX_LENGTH = 50
MAX_LENGTH_NAME = 255
MAX_USERNAME_LENGTH = 150
MAX_LENGTH_SLUG = 50
RESTRICTED_NAMES = ('me',)
USERNAME_PATTERN = re.compile(r'\w{1,150}')
EMAIL_PATTERN = re.compile(r'\w+[.|_]?\w+@\w+\.[A-Z|a-z]{2,}')
EMAIL_FROM = 'somestuff@yambd.mcd'
EMAIL_SUBJECT = 'Confirmation code for yambd.'
ADMIN = 'admin'
MODER = 'moderator'
USER = 'user'
