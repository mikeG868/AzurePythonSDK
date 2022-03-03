import os
import random
import string

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

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
compute_client = ComputeManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)

def listVMs():
    #list VNets
    VNets = list(compute_client.virtual_machines.list(GROUP_NAME))
    for i in VNets:
        print("VMs: {}".format(i.name))

def createVM(GROUP_NAME):
    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    ).result()

    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    ).result()

    # Create network interface
    network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        INTERFACE_NAME,
        {
            'location': "eastus",
            'ip_configurations': [{
                'name': 'MyIpConfig',
                'subnet': {
                    'id': subnet.id
                }
            }]
        } 
    ).result()

    # Create virtual machine
    vm = compute_client.virtual_machines.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        {
          "location": "eastus",
          "hardware_profile": {
            "vm_size": "Standard_D2_v2"
          },
          "storage_profile": {
            "image_reference": {
              "sku": "2016-Datacenter",
              "publisher": "MicrosoftWindowsServer",
              "version": "latest",
              "offer": "WindowsServer"
            },
            "os_disk": {
              "caching": "ReadWrite",
              "managed_disk": {
                "storage_account_type": "Standard_LRS"
              },
              "name": "myVMosdisk",
              "create_option": "FromImage"
            },
            "data_disks": [
              {
                "disk_size_gb": "1023",
                "create_option": "Empty",
                "lun": "0"
              },
              {
                "disk_size_gb": "1023",
                "create_option": "Empty",
                "lun": "1"
              }
            ]
          },
          "os_profile": {
            "admin_username": "testuser",
            "computer_name": "myVM",
            "admin_password": your_password,
            "windows_configuration": {
              "enable_automatic_updates": True  # need automatic update for reimage
            }
          },
          "network_profile": {
            "network_interfaces": [
              {
                "id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + GROUP_NAME + "/providers/Microsoft.Network/networkInterfaces/" + INTERFACE_NAME + "",
                # "id": NIC_ID,
                "properties": {
                  "primary": True
                }
              }
            ]
          }
        }
    ).result()
    print("Create virtual machine:\n{}".format(vm))

    # Create vm extension
    extension = compute_client.virtual_machine_extensions.begin_create_or_update(
        GROUP_NAME,
        VIRTUAL_MACHINE_NAME,
        VIRTUAL_MACHINE_EXTENSION_NAME,
        {
          "location": "eastus",
          "auto_upgrade_minor_version": True,
          "publisher": "Microsoft.Azure.NetworkWatcher",
          "type_properties_type": "NetworkWatcherAgentWindows",  # TODO: Is this a bug?
          "type_handler_version": "1.4",
        }
    ).result()
    print("Create vm extension:\n{}".format(extension))

def startVM(GROUP_NAME,VM_NAME):
    async_vm_stop = compute_client.virtual_machines.begin_power_off(GROUP_NAME, VM_NAME)
    async_vm_stop.wait()

def stopVM(GROUP_NAME,VM_NAME):
    async_vm_start = compute_client.virtual_machines.begin_start(GROUP_NAME, VM_NAME)
    async_vm_start.wait()   


if __name__ == '__main__':

    GROUP_NAME = "mikeRG"
    VIRTUAL_MACHINE_NAME = "virtualmachinex"
    SUBNET_NAME = "subnetx"
    INTERFACE_NAME = "interfacex"
    NETWORK_NAME = "networknamex"
    VIRTUAL_MACHINE_EXTENSION_NAME = "virtualmachineextensionx"

    your_password = 'A1_' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

    listVMs()
    # createVM(GROUP_NAME)
    # startVM(GROUP_NAME,VIRTUAL_MACHINE_NAME)
    # stopVM(GROUP_NAME,VIRTUAL_MACHINE_NAME)
