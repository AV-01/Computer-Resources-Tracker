# This module writes all the data to a file
import time
import load_resources as load
import csv
from datetime import datetime

# time,name,pid,mem,vms,cpu
# time,cpu,net_in,net_out,ram percent,ram gb


def write_data(getCPU, getRAM, getNetwork, getProcess):
    now = str(datetime.now()).split('.')[0]
    computer_data = [now]
    if getCPU:
        computer_data.append(load.cpu_usage())
    else:
        computer_data.append(None)
    if getNetwork:
        net_use = load.net_usage()
        computer_data.append(net_use['recieve'])
        computer_data.append(net_use['send'])
    else:
        computer_data.append(None)
        computer_data.append(None)
    if getRAM:
        ram_use = load.ram_usage()
        computer_data.append(ram_use['Percentage'])
        computer_data.append(ram_use['Used'])
    else:
        computer_data.append(None)
        computer_data.append(None)
    process_data = []
    if getProcess:
        processInfo = load.getProcesses()
        zombieProc = []
        zombProcesses = load.findZomb()
        for i in zombProcesses:
            info = [i['name']]
            zombieProc.append(info)
        with open('zombie_resources.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerows(zombieProc)
        for i in processInfo:
            info = [str(now),i['name'],i['pid'],i['mem'],i['vms'],i['cpu_usg']]
            process_data.append(info)
        with open('process_data.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerows(process_data)
    else:
        process_data.append(None)
    with open('computer_data.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(computer_data)

write_data(False,False,False, True)
