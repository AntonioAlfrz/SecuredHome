import ConfigParser
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import subprocess

Config = ConfigParser.ConfigParser()
Config.read("creds.ini")
section = "Azure"

container = Config.get(section, "container")
base_url = Config.get(section, "base_url") + container + "/"
block_blob_service = None


def init():
    global block_blob_service
    account = Config.get(section, "myaccount")
    key = Config.get(section, "account_key")
    block_blob_service = BlockBlobService(
        account_name=account, account_key=key)
    print "\nAzure Storage set"


def upload(name, path):
    print "\nAzure uploading"
    block_blob_service.create_blob_from_path(
        container,
        name,
        path,
        content_settings=ContentSettings(content_type='image/jpeg')
    )


def list_blobs():
    generator = block_blob_service.list_blobs(container)
    for blob in generator:
        return base_url + blob.name
