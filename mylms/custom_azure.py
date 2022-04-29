from storages.backends.azure_storage import AzureStorage
from django.conf import settings

class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME # Must be replaced by your <storage_account_name>
    account_key = settings.AZURE_STORAGE_ACCOUNT_KEY # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
    # file_overwrite = False

class AzureStaticStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME # Must be replaced by your storage_account_name
    account_key = settings.AZURE_STORAGE_ACCOUNT_KEY # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
    # file_overwrite = False