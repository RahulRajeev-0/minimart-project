
from decouple import config

environment = config('DJANGO_ENVIRONMENT', 'development')

# print(environment)

if environment == 'production':
    print("working production")
    from .production import *
else:
    print("working development")
    from .development import *