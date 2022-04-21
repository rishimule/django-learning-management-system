from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'lmsdjangoaccountstorage' # Must be replaced by your <storage_account_name>
    account_key = 'K0xDIB/z2pVupQT/83rStMOcl+mR7kaYIbQQyODHl+FfpjvhBsHQfYvFaFslLoKb22a6K681Bg3LRgkzQrMdng==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
    # file_overwrite = False

class AzureStaticStorage(AzureStorage):
    account_name = 'lmsdjangoaccountstorage' # Must be replaced by your storage_account_name
    account_key = 'K0xDIB/z2pVupQT/83rStMOcl+mR7kaYIbQQyODHl+FfpjvhBsHQfYvFaFslLoKb22a6K681Bg3LRgkzQrMdng==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
    # file_overwrite = False