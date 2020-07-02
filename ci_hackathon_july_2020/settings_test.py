from .settings import *

# test should use a local db
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'TEST': {
                'NAME': 'mytestdatabase',
            },
        }
    }

# test should use local storage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
SECRET_KEY = "abc123"

# test uses nose to get coverage
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=accounts,challenges,checkout,home,products,ratings,submissions',
]