
SECRET_KEY = 'exposed-secret-key-1234'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.sessions','django.contrib.staticfiles','storeapp']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}