# This module has all the functions needed to get all the resources
import psutil
import time
import os
import signal
# Get percentage of CPU being used:
def cpu_usage():
    return psutil.cpu_percent(1)

def ram_usage():
    ram_data = psutil.virtual_memory()
    return {"Percentage":ram_data[2],"Used":ram_data[3]/1000000000}

# Get network usage data
def net_usage():
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)["Wi-Fi"]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    time.sleep(1)
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)["Wi-Fi"]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent

    net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
    net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
    return {"recieve":net_in,"send":net_out}

def getProcesses():
    processes = []
    for process in psutil.process_iter():
       try:
           pinfo = process.as_dict(attrs=['pid', 'name'])
           pinfo['mem'] = process.memory_info().rss / (1024 * 1024) # RSS is the resident set size
           pinfo['vms'] = process.memory_info().vms / (1024 * 1024) #vms is for accessing virtual memory usage
           pinfo['cpu_usg'] = process.cpu_percent()/psutil.cpu_count()
           processes.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    processes = sorted(processes, key=lambda procObj: procObj['vms'], reverse=True)
    return processes[:5]

def findZomb():
    processes = []
    for process in psutil.process_iter():
       try:
           pinfo = process.as_dict(attrs=['pid', 'name'])
           # pinfo['mem'] = process.memory_info().rss / (1024 * 1024) # RSS is the resident set size
           pinfo['vms'] = process.memory_info().vms / (1024 * 1024) #vms is for accessing virtual memory usage
           pinfo['cpu_usg'] = process.cpu_percent()/psutil.cpu_count()
           if pinfo['cpu_usg'] == 0.0 and pinfo['vms']<25:
               processes.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    processes = sorted(processes, key=lambda procObj: procObj['vms'], reverse=True)
    return processes[:5]
    # return processes
    # Sort list of dict by key vms i.e. memory usage
# for i in findZomb():
    # os.kill(i['pid'], signal.SIGKILL)
# print(findZomb())
