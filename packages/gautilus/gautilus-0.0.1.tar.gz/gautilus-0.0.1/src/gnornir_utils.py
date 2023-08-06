"""
    Utilities to initialize nornir inventories and load passwords; print results to .json files.
    - garrettl
"""

import subprocess
import json
from nornir import InitNornir
import boto3
from botocore.config import Config



def nornir_init(cloud, region):
    """ 
    NORNIR INITIALIZE
    Takes:
        cloud: cloud provider, currently AWS or GCP
        region: cloud region, with provider specific naming conventions
    Outputs:
        Nornir object with inventory, pull passwords
    """
    inv_path = "/home/garrettl/repos/stamp_audit/inventory/nornir_inventories"

    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{inv_path}/{region}.yaml",
                "group_file": "groups.yaml"
            },
        },
    )
    print(cloud)
    if cloud == "GCP":
        berglas_nornir_passwords(nr)
    elif cloud == "AWS":
        aws_nornir_passwords(nr, region)

    return nr


def berglas_nornir_passwords(norn):
    """ 
    GET BERGLAS PASSWORDS
    Takes:
        norn: Initialized Nornir object with inventory loaded
    Outputs:
        Nornir object with passwords added to the inventory
    """
    print("Initializing.....")
    for host in norn.inventory.hosts:
        try:
            secret = subprocess.run(["berglas", "access", f"gcp-secrets-bucket/{host}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=True,
                text=True
            )

            pwd = json.loads(secret.stdout)
            norn.inventory.hosts[host].password = pwd['Password']
        except:
            norn.inventory.hosts[host].password = ""
    print(".....passwords loaded.")


def aws_nornir_passwords(norn, region):
    """ 
    GET AWS PASSWORDS
    Takes:
        norn: Initialized Nornir object with inventory loaded
        region: needs aws region to query secrets manager
    Outputs:
        Nornir object with passwords added to the inventory
    """
    print("Initializing.....")
    my_config = Config(region_name = region)
    client = boto3.client('secretsmanager', config=my_config)

    for host in norn.inventory.hosts:
        try:
            response = client.get_secret_value(
                SecretId = host
            )
            output = response['SecretString'].replace('\\', '').replace('"{', '{').replace('}"', '}').replace('\n', '')
            secret = json.loads(output)
            norn.inventory.hosts[host].password = secret[list(secret.keys())[0]]['Password']
        except Exception as e:
            print(e)
            norn.inventory.hosts[host].password = ""
    print(".....passwords loaded.")


def nornir_pre_init():
    """ 
    NORNIR PRE-INITIALIZE
    Takes:
        none
    Outputs:
        Nornir object with inventory, pull passwords from respective secrets manager
    """
    inv_path = "./inventory/"
    inv_file = "ISR-global.yaml"

    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": inv_path + inv_file,
                "group_file": f"{inv_path}groups.yaml"
            },
        },
    )
    return nr


def load_secrets(norn):
    """ 
    LOAD SECRETS
    Takes:
        norn: Inventory from an initialized Nornir object
    Outputs:
        Password from berglas to be added to the Nornir inventory; with intent to be added after inventory is filtered
    """
    for host in norn.inventory.hosts:
        print(f"Gettings secret for {host}")
        if norn.inventory.hosts[host].data['cloud'] == "gcp":
            password = berglas_nornir_passwords(host)
            norn.inventory.hosts[host].password = password
        elif norn.inventory.hosts[host].data['cloud'] == "aws":
            password = aws_nornir_passwords(host, norn.inventory.hosts[host].data['region'])
            norn.inventory.hosts[host].password = password
    
    return norn


def berglas_nornir_passwords(host):
    """ 
    GET BERGLAS PASSWORD
    Takes:
        host: Singular host from an initialized Nornir object
    Outputs:
        Password from berglas to be added to the Nornir inventory
    """
    secret = subprocess.run(["berglas", "access", f"gcp-secrets-bucket/{host}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=True,
        text=True
    )
    pwd = json.loads(secret.stdout)

    return pwd['Password']
    


def aws_nornir_passwords(host, region):
    """ 
    GET AWS PASSWORD
    Takes:
        host: Singular host from an initialized Nornir object
        region: needs aws region to query secrets manager
    Outputs:
        Password from AWS secrets manager to be added to the Nornir inventory
    """

    my_config = Config(region_name = region)
    client = boto3.client('secretsmanager', config=my_config)

    response = client.get_secret_value(
        SecretId = host
    )
    output = response['SecretString'].replace('\\', '').replace('"{', '{').replace('}"', '}').replace('\n', '')
    secret = json.loads(output)

    return secret[list(secret.keys())[0]]['Password']


def inventory_regions(norn):
    pass    



def output_to_json(name, data):
    """ 
    OUTPUT TO JSON
    Takes:
        name: name to pass to .json file; usually the region
        data: Nornir results objects to turn into a dict with list of results dicts
    Outputs:
        .json artifacts of Nornir results to be manipulated/viewd later without having to recall jobs constantly
    """
    results_dict = {}

    for host in data:
        results_dict[host] = []
        for i in range(len(data[host])):
            if data[host][i].result:
                results_dict[host].append(data[host][i].result)
    
    with open(f"./artifacts/{name}.json", "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2)
    
    print(f"./artifacts/{name}.json created.")


def pick_cloud():
    """ 
    PICK CLOUD
    Takes:
        none
    Returns:
        integer index of cloud selected
    """
    provider_index = 0
    provider_list = ["GCP", "AWS"]

    for i in range(2):
        print(f"[{i}] {provider_list[i]}")
    provider_index = int(input("Choose index of cloud provider: "))
    return provider_index
    

def pick_region(provider_index):
    """ 
    PICK REGION
    Takes:
        provider_index: index from list of cloud providers
    Returns:
        string name of cloud region selected
    """
    gcp_regions = ['asia-northeast1', 'australia-southeast1', 'europe-west2', 'europe-west3', 'europe-west4',
        'northamerica-northeast1', 'us-central1', 'us-east4', 'us-west2', 'us-west3', 'us-west4'
    ]
    aws_regions = ['us-east-1', 'us-west-1', 'us-west-2', 'eu-central-1', 'eu-west-1', 'eu-west-2',
        'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1'
    ]
    all_regions = [gcp_regions, aws_regions]

    for i in range(len(all_regions[provider_index])):
        print(f"[{i}] {all_regions[provider_index][i]}")
    region_index = input("Pick a region: ")
    try:
        region = all_regions[provider_index][int(region_index)]
    except:
        region = region_index

    return region




if __name__ == "__main__":
    pass

    
    
    
