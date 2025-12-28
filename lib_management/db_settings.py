# PostgreSQL Database settings for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'library_user',
        'PASSWORD': 'root',
        'HOST': 'host.docker.internal',
        'PORT': '5432',
    }
}
