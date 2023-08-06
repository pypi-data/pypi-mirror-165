"""
    Generate excel reports for auditing.
    - garrettl
"""

import json
import pandas

inv_path = "/home/garrettl/repos/stamp_audit/inventory"
key_path = "/home/garrettl/repos/keys"


def std_report(input_file):
    """ 
    STANDARD REPORT
    Takes:
        input_file: .json
    Outputs:
        JSON to Excel .xml
    """
    with open(input_file, "r") as f:
        data = json.load(f)

    # All arrays must be of the same length
    #df = pandas.read_json(input_file)
    df = data['GCP-asia-northeast-1-MGMT01']

    df_data = pandas.json_normalize(df, record_path=['get_arp_table'])
    print(df_data)



def report1(input_file):
    """ 
    REPORT 1
    Takes:
        input_file: .json from Napalm "facts" getter
    Outputs:
        pandas dataframe with regional hostnames, management interfaces, and IP addresses
    """
    with open(input_file, "r") as f:
        data = json.load(f)
    df_data = []

    for host in data:
        try:
            row = [host, data[host][0]['facts']['hostname']]
            
            for interface in data[host][0]['get_interfaces_ip']:            
                ip_addrs = data[host][0]['get_interfaces_ip'][interface]['ipv4'].keys()
                filler = ["", ""]

                for ip in ip_addrs:
                    if "192.168." in ip or "172.30." in ip:
                        if len(row) > 3:
                            filler.append(interface)
                            filler.append(ip)
                            df_data.append(filler)
                            filler = ["", ""]
                        else:
                            row.append(interface)
                            row.append(ip)
                            df_data.append(row)
        except TypeError:
            continue

    data_frame = pandas.DataFrame(df_data, columns=["Secret ID", "Hostname", "Mgmt Intf's", "Mgmt IP Addr's"])
    return data_frame


def report2(input_file1, inputfile2):
    """ 
    REPORT 2
    Takes:
        inputfile1: .json from Napalm "get_arp_table" getter
        inputfile2: .json from Napalm "facts" and "get_interfaces_ip" getters
    Outputs:
        dataframe with arp table of given hosts
        also matches the ARP IP entries to host entries
    """
    with open(input_file1, "r") as f:
        data = json.load(f)
    df_data = []

    match_ip = reverse_ip_lookup(inputfile2)

    for host in data:
        row = [host]

        for entry in data[host][0]['get_arp_table']:
            #print(entry)        
            filler = [""]
            if len(row) > 2:
                filler.append(entry['interface'])
                filler.append(entry['mac'])
                filler.append(entry['ip'])
                filler.append(entry['age'])
                filler.append(str(match_ip.get(entry['ip'], "")).strip("[]").replace("'", ""))
                df_data.append(filler)
            else:
                row.append(entry['interface'])
                row.append(entry['mac'])
                row.append(entry['ip'])
                row.append(entry['age'])
                row.append(str(match_ip.get(entry['ip'], "")).strip("[]").replace("'", ""))
                df_data.append(row)
        
    data_frame = pandas.DataFrame(df_data, columns=["Host", "Interface", "MAC", "IP Address", "Age (s)", "Associated Hosts"])
    return data_frame


def nornir_failed_hosts(input_file):
    """ 
    FAILED HOSTS
    Takes:
        input_file as json file extracted from Nornir failed hosts object
    Outputs:
        pandas dataframe with table of failed hosts for each task
    """
    with open(input_file, "r") as f:
        data = json.load(f)
    df_data = []

    for host in data:
        row = [host, data[host][0]]
        df_data.append(row)


    data_frame = pandas.DataFrame(df_data, columns=["Host", "Error"])
    return data_frame



def gen_report(output_file, df_list, tabs_list=[]):
    """ 
    REPORT GENERATOR
    Takes:
        output_file name as str
        df_list list of pandas dataframes
        tabs_list (optional) list of str's to name sheets, in order of corresponding dataframes
    Outputs:
        excel spreadsheet combining report datasets
    """
    with pandas.ExcelWriter(f'./reports/g1/{output_file}.xlsx') as writer:
        if len(tabs_list) > 0:
            for df, tab in zip(df_list, tabs_list):
                df.to_excel(writer, sheet_name=tab, index=False)
        else:
            for df in df_list:
                df.to_excel(writer, index=False)


    print(f'./reports/{output_file}.xlsx created')


# Packaging for easy importation by gather_hostnames.py
def combo1(region):
    file1 = f"./artifacts/g1/{region}_1.json"
    file2 = f"./artifacts/g1/{region}_2.json"
    file3 = f"./artifacts/g1/{region}_FAILED_1.json"
    file4 = f"./artifacts/g1/{region}_FAILED_2.json"
    
    gen_report(region, 
        [
            report1(file1), 
            report2(file2, file1), 
            nornir_failed_hosts(file3), 
            nornir_failed_hosts(file4)
        ], 
        [
            "MGMT Info", 
            "ARP Info", 
            "FAILED Hosts Task1", 
            "FAILED Hosts Task2"
        ]
    )


def reverse_ip_lookup(input_file):
    """ 
    CREATE REVERSE IP LOOKUP
    Takes:
        input_file: .json from Napalm "facts" getter, same input as Report1
    Outputs:
        python dict with each IP address as key and the hostname as value, to compare IPs later.
    """
    with open(input_file, "r") as f:
        data = json.load(f)
    ip_dict = {}

    for host in data:
        try:          
            for interface in data[host][0]['get_interfaces_ip']:            
                ip_addrs = list(data[host][0]['get_interfaces_ip'][interface]['ipv4'])

                if ip_addrs:
                    for ip in ip_addrs:
                        if ip_dict.get(ip):
                            ip_dict[ip].append(data[host][0]['facts']['hostname'])
                        else:
                            ip_dict[ip] = [data[host][0]['facts']['hostname']]
        except TypeError:
            continue

    return ip_dict



if __name__ == "__main__":
    gcp_regions = ['asia-northeast1', 'australia-southeast1', 'europe-west2', 'europe-west3', 'europe-west4', 
        'northamerica-northeast1', 'us-central1', 'us-east4', 'us-west2', 'us-west3', 'us-west4'
    ]

    file = f"./artifacts/g1/{gcp_regions[0]}_2.json"

    std_report(file)

