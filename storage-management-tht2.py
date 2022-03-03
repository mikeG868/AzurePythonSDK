import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient

SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

# Create client
resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)
storage_client = StorageManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)

def createRG(GROUP_NAME):
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "northeurope"}
    )

def getBlobContainers(storage_client,GROUP_NAME,STORAGE_ACCOUNT):
    # List storage groups
    blobs = list(storage_client.blob_containers.list(GROUP_NAME,STORAGE_ACCOUNT))
    for i in blobs:
        print("Blob: {}".format(i.name))

def createStorageAndBlob(storage_client,GROUP_NAME,STORAGE_ACCOUNT,BLOB_CONTAINER):
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
          "sku": {
            "name": "Standard_GRS"
          },
          "kind": "StorageV2",
          "location": "eastus",
          "encryption": {
            "services": {
              "file": {
                "key_type": "Account",
                "enabled": True
              },
              "blob": {
                "key_type": "Account",
                "enabled": True
              }
            },
            "key_source": "Microsoft.Storage"
          },
          "tags": {
            "key1": "value1",
            "key2": "value2"
          }
        }
    ).result()

    # - end -
    blob_container = storage_client.blob_containers.create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER,
        {}
    )
    print("Create blob container:\n{}".format(blob_container))

def uploadfile(BLOB_CONTAINER,name,cstr,filename):
    blob = BlobClient.from_connection_string(conn_str=cstr, container_name=BLOB_CONTAINER, blob_name=name)

    with open(filename, "rb") as data:
        blob.upload_blob(data)
    print("Uploaded file to: {}".format(filename))

def downloadfile(BLOB_CONTAINER,name,cstr,downfile):
    blob = BlobClient.from_connection_string(conn_str=cstr, container_name=BLOB_CONTAINER, blob_name=name)

    with open(downfile, "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
   
    print("Downloaded file to: {}".format(downfile))

def deleteBlob(BLOB_CONTAINER,name,cstr):
    blob = BlobClient.from_connection_string(conn_str=cstr, container_name=BLOB_CONTAINER, blob_name=name)
    blob_data = blob.delete_blob()
    print("Deleted blob: {}".format(name))

def deleteContainer(storage_client,GROUP_NAME,STORAGE_ACCOUNT,BLOB_CONTAINER):
    blob_container = storage_client.blob_containers.delete(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER
    )
    print("Deleted blob container: {}".format(BLOB_CONTAINER))

if __name__ == '__main__':

    GROUP_NAME = "mikeRG-storage"
    STORAGE_ACCOUNT = "mikestorageawacademy"
    BLOB_CONTAINER = "mike-blobcontainer"

    #createRG(GROUP_NAME)
    #getBlobContainers(storage_client,GROUP_NAME,STORAGE_ACCOUNT)
    #createStorageAndBlob(storage_client,GROUP_NAME,STORAGE_ACCOUNT,BLOB_CONTAINER)

    blob_name="picture.png"
    cstr= "BlobEndpoint=https://mikestorageawacademy.blob.core.windows.net/;QueueEndpoint=https://mikestorageawacademy.queue.core.windows.net/;FileEndpoint=https://mikestorageawacademy.file.core.windows.net/;TableEndpoint=https://mikestorageawacademy.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bf&srt=sco&sp=rwdlacitfx&se=2022-03-05T05:07:14Z&st=2022-03-03T21:07:14Z&spr=https&sig=fDiE68SumnfZqkJVMq2QvFLL99BT6GabALcS7Z9Tyf0%3D"
    filename = "./sample.png"
    downfile = "./downsample.png"
    #uploadfile(BLOB_CONTAINER,blob_name,cstr,filename)
    #downloadfile(BLOB_CONTAINER,blob_name,cstr,downfile)
    #deleteBlob(BLOB_CONTAINER,blob_name,cstr)
    
    #deleteContainer(storage_client,GROUP_NAME,STORAGE_ACCOUNT,BLOB_CONTAINER)


