from .settings import *

STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
