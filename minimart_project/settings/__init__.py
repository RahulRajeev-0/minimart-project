
from decouple import config

environment = config('DJANGO_ENVIRONMENT', 'development')

# print(environment)

if environment == 'production':
    from .production import *
else:
    from .development import *