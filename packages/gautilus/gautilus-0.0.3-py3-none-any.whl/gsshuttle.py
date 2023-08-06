"""
    Open and close sshuttle forwarding tunnels with python.
    - garrettl
"""

import os
import sys
import json
import signal
import subprocess
from subprocess import CalledProcessError
from gnornir_utils import pick_cloud, pick_region


def precheck():
    """ 
    PRECHECK
    Takes:
        none
    Returns:
        none
    Does:
        Checks if sshuttle is installed on the system.
    """
    try:
        subprocess.check_output(["which", "sshuttle"]).strip()
    except CalledProcessError:
        print("sshuttle is not installed on this host")
        sys.exit()


# Only fully works with AWS
def start_Async(regions, conf):
    """ 
    START ASYNCHRONOUS TUNNEL
    Takes:
        regions: list of regions to create tunnels to
        conf: configuration file > .json with regional jumphost and subnet data
    Returns:
        none
    Does:
        Creates sshuttle tunnels to each region as child processes in the background, forwarding traffic for each subnet provided.
    """
    with open(conf) as f:
        jh_data = json.load(f)
    
    for region in regions:
        networks = jh_data[region]['stamp_subnets']
        rhost = jh_data[region]['jumphost_ip']

        rpath = f"{rhost} {' '.join(networks)}"
        try:
            print("starting sshuttle..")
            subprocess.Popen(f"sshuttle -r {rpath}", shell=True)
        except Exception as e:
            print(e)


def start_static(region, conf):
    """ 
    START STATIC TUNNEL
    Takes:
        region: string of region to create single tunnel to
        conf: configuration file > .json with regional jumphost and subnet data
    Returns:
        none
    Does:
        Creates sshuttle tunnel to a region as the main process, forwarding traffic for each subnet provided.
        Nothing else will execute within the same program whilst this is running.
    """
    with open(conf) as f:
        jh_data = json.load(f)
        
    networks = jh_data[region]['stamp_subnets']
    rhost = jh_data[region]['jumphost_ip']

    try:
        print("starting sshuttle..")
        subprocess.run(["sshuttle", "-r", rhost, *networks],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True,
            text=True
        )
    except Exception as e:
        print(e)


def get_pid():
    """ 
    GET PID
    Takes:
        none
    Returns:
        List of process IDs for running sshuttle tunnels.
    """
    search = "ps -ef | grep '/usr/bin/python3 /usr/bin/sshuttle -r' | grep -v grep | awk {'print $2'}"    
    pids = []
    for line in os.popen(search):
        fields = line.split()
        pids.append(fields[0])
    return pids


def stop():
    """ 
    GET PID
    Takes:
        none
    Returns:
        none
    Does:
        Stops all running sshuttle processes.
    """
    pids = get_pid()
    for pid in pids:
        print(f"stopping sshuttle PID {pid}")
        os.kill(int(pid), signal.SIGTERM)


def status():
    """ 
    GET PID
    Takes:
        none
    Returns:
        none
    Does:
        Prints status of sshuttle; whether there are instances running or not.
    """
    pids = get_pid()
    if pids:
        print("sshuttle is running..")
    else:
        print("sshuttle is not running..")



if __name__ == "__main__":

    precheck()
    cmd = input("sshuttle:: start: (static | async) | stop | status: \n: ").lower().strip()

    if cmd == "start" or cmd == "static":
        start_static(pick_region(pick_cloud()), "/home/garrettl/repos/stamp_audit/inventory/stamp_regions.json")
    elif cmd == "async":
        start_Async(['us-central1', 'asia-northeast1'], "/home/garrettl/repos/stamp_audit/inventory/stamp_regions.json")
    elif cmd == "stop":
        stop()
    elif cmd == "status":
        status()
