import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

#listaa kaikki RG resut
def listRG():
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # List resource groups
    resource_groups = list(resource_client.resource_groups.list())
    #print("List resource groups:\n{}".format(resource_groups))
    
    for i in resource_groups:
        print(i)
        print("Name: {}\nLocation: {}\nTags: {}\n".format(i.name, i.location, i.tags))


def createRG(RGname):

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    rg_result = resource_client.resource_groups.create_or_update(
        RGname,
        {
            "location": "northeurope",
        }
    )

    print(f"Create resource group {rg_result.name} without tags")
    
def getRG(RGname):

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # List resource groups
    resource_groups = list(resource_client.resource_groups.list())
    
    for i in resource_groups:
        if RGname == i.name:
            print("Name: {}\nLocation: {}\nTags: {}\n".format(i.name, i.location, i.tags))

def updateRGTag(RGname):
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    rg_result = resource_client.resource_groups.create_or_update(
        RGname,
        {
            "location": "northeurope",
            "tags": { "environment":"test", "department":"AWAcademy" }
        }
    )

def deleteRG(RGname):
    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    delete_async_operation = resource_client.resource_groups.begin_delete(RGname)
    delete_async_operation.wait()

if __name__ == "__main__":
    RG = "mikeRG-python"
    #listRG()
    #createRG(RG)
    #getRG(RG)
    #updateRGTag(RG)
    deleteRG(RG)