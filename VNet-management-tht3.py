import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient

SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
# Create client
resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)
network_client = NetworkManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)

def listVNets(network_client,GROUP_NAME):
    #list VNets
    VNets = list(network_client.virtual_networks.list(GROUP_NAME))
    for i in VNets:
        print("VNets: {}".format(i.name))

def createVnet(VIRTUAL_NETWORK_NAME,vnetaddr):
    network = network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        {
          "address_space": {
            "address_prefixes": [
                vnetaddr
            ]
          },
          "location": "eastus"
        }
    ).result()
    print("Create virtual network:\n{}".format(network))

def createSubnet(VIRTUAL_NETWORK_NAME,SUBNET,subnetaddr):
    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET,
        {
            "address_prefix": subnetaddr
        }
    ).result()
    print("Create subnet:\n{}".format(subnet))

def deleteSubnet(SUBNET):
    subnet = network_client.subnets.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME,
        SUBNET
    ).result()
    print("Delete subnet.\n")

def deleteVNet(VIRTUAL_NETWORK_NAME):
    network_client.virtual_networks.begin_delete(
        GROUP_NAME,
        VIRTUAL_NETWORK_NAME
    ).result()
    print("Delete virtual network.\n")

if __name__ == '__main__':

    GROUP_NAME = "mikeRG"
    VIRTUAL_NETWORK_NAME = "virtualnetwork"
    SUBNET = "subnetxxyyzz"

    listVNets(network_client,GROUP_NAME)

    vnetaddr = "100.0.0.0/16"
    subnetaddr = "100.0.0.0/24"
    #createVnet(VIRTUAL_NETWORK_NAME,vnetaddr)
    #createSubnet(VIRTUAL_NETWORK_NAME,SUBNET,subnetaddr)
    #deleteSubnet(SUBNET)
    #deleteVNet(VIRTUAL_NETWORK_NAME)