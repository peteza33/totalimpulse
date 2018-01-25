from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage

class GCSStaticStorage(GoogleCloudStorage):
    bucket_name = settings.GS_BUCKET_PREFIX + '_static'

class GCSMediaStorage(GoogleCloudStorage):
    bucket_name = settings.GS_BUCKET_PREFIX + '_media'