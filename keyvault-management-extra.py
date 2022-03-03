import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient

SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
TENANT_ID = os.environ.get("AZURE_TENANT_ID", None)

# Create client
resource_client = ResourceManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)
keyvault_client = KeyVaultManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)
def listVaults(GROUP_NAME):
    vaults = list(keyvault_client.vaults.list())
    for i in vaults:
        print("Vault: {}".format(i.name))

def createVault(GROUP_NAME,VAULT):
    # Create vault
    vault = keyvault_client.vaults.begin_create_or_update(
        GROUP_NAME,
        VAULT,
        {
          "location": "eastus",
          "properties": {
            "tenant_id": TENANT_ID,
            "sku": {
              "family": "A",
              "name": "standard"
            },
            "access_policies": [
              {
                "tenant_id": TENANT_ID,
                "object_id": "00000000-0000-0000-0000-000000000000",
                "permissions": {
                  "keys": [
                    "encrypt",
                    "decrypt",
                    "wrapKey",
                    "unwrapKey",
                    "sign",
                    "verify",
                    "get",
                    "list",
                    "create",
                    "update",
                    "import",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge"
                  ],
                  "secrets": [
                    "get",
                    "list",
                    "set",
                    "delete",
                    "backup",
                    "restore",
                    "recover",
                    "purge"
                  ],
                  "certificates": [
                    "get",
                    "list",
                    "delete",
                    "create",
                    "import",
                    "update",
                    "managecontacts",
                    "getissuers",
                    "listissuers",
                    "setissuers",
                    "deleteissuers",
                    "manageissuers",
                    "recover",
                    "purge"
                  ]
                }
              }
            ],
            "enabled_for_deployment": True,
            "enabled_for_disk_encryption": True,
            "enabled_for_template_deployment": True
          }
        }
    ).result()
    print("Create vault:\n{}".format(vault))

def deleteVault(GROUP_NAME, VAULT):
    keyvault_client.vaults.delete(
        GROUP_NAME,
        VAULT
    )
    print("Delete vault.\n")


if __name__ == '__main__':

    GROUP_NAME = "mikeRG-storage"
    VAULT = "mykeyvault-mike"

    #listVaults(GROUP_NAME)
    #createVault(GROUP_NAME,VAULT)
    deleteVault(GROUP_NAME, VAULT)