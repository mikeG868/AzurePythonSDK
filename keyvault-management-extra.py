import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault.secrets import SecretClient

SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
TENANT_ID = os.environ["AZURE_TENANT_ID"]
keyVaultName = os.environ["KEY_VAULT_NAME"]

# Create client
keyvault_client = KeyVaultManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=SUBSCRIPTION_ID
)

KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=KVUri, credential=credential)


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
          "location": "northeurope",
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

def createSecret(secretName,secret_client):
  secretValue = input("Input a value for your secret > ")
  print(f"Creating a secret in {keyVaultName} called '{secretName}' with the value '{secretValue}' ...")

  secret_client.set_secret(secretName, secretValue)

  print(" done.")

def retrieveSecret(secretName,secret_client):
  print(f"Retrieving your secret from {keyVaultName}.")

  retrieved_secret = secret_client.get_secret(secretName)

  print(f"Your secret is '{retrieved_secret.value}'.")

def deleteSecret(secretName,secret_client):
  print(f"Deleting your secret from {keyVaultName} ...")

  poller = secret_client.begin_delete_secret(secretName)
  deleted_secret = poller.result()

  print(" done.")


if __name__ == '__main__':

  GROUP_NAME = "mikeRG"
  VAULT = "keyvault-mikeAW"

  #listVaults(GROUP_NAME)
  #createVault(GROUP_NAME,VAULT)
  # deleteVault(GROUP_NAME, VAULT)

  secretName = input("Input a name for your secret > ")

  # createSecret(secretName,secret_client)
  retrieveSecret(secretName,secret_client)
  # deleteSecret(secretName,secret_client)