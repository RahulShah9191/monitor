import os
import subprocess
import shutil
from datetime import datetime

_statistics = {}
_file_path = '/tmp/monitor.csv'
_header_line = "date_time,physical_and_logical_cpu_count,cpu_load,physical_total_mem(bytes),physical_used_mem(bytes),physical_free_mem(bytes),physical_shared_mem(bytes),physical_buff_cached_available(bytes),swap_total_mem(bytes),swap_used_mem(bytes),swap_free_mem(bytes),swap_buff_cached_available(bytes),total_disk(GB),used_disk(GB),free_disk(GB),network_min_latency(ms),network_avg_latency(ms),network_max_latency(ms)"

def _get_cpu_info():
    # Get Physical and Logical CPU Count
    physical_and_logical_cpu_count = os.cpu_count()
    _statistics['physical_and_logical_cpu_count'] = physical_and_logical_cpu_count
    cpu_load = [x / os.cpu_count() * 100 for x in os.getloadavg()][-1]
    _statistics['cpu_load'] = cpu_load

def _get_mem_info():
    free_command = subprocess.run(['free'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    _statistics['physical_total_mem'] = free_command[1].split()[1]
    _statistics['physical_used_mem'] = free_command[1].split()[2]
    _statistics['physical_free_mem'] = free_command[1].split()[3]
    _statistics['physical_shared_mem'] = free_command[1].split()[4]
    _statistics['physical_buff_cached_available'] =  free_command[1].split()[5]
    _statistics['swap_total_mem'] = free_command[2].split()[1]

    _statistics['swap_used_mem'] = free_command[2].split()[2]
    _statistics['swap_free_mem'] = free_command[2].split()[3]
    try:
        _statistics['swap_free_mem'] = free_command[2].split()[4]
    except:
        _statistics['swap_free_mem'] = None
    try:
        _statistics['swap_buff_cached_available'] = free_command[2].split()[4]
    except:
        _statistics['swap_buff_cached_available']  = None


def _get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    _statistics['total_disk'] = round(total / 1024 ** 3, 1)
    _statistics['used_disk'] = round(used / 1024 ** 3, 1)
    _statistics['free_disk'] = round(free / 1024 ** 3, 1)


def _get_netork_info():
    ping_result = subprocess.run(['ping', '-i 5', '-c 5', 'google.com'], stdout=subprocess.PIPE).stdout.decode(
        'utf-8').split('\n')
    min, avg, max = ping_result[-2].split('=')[-1].split('/')[:3]
    _statistics['network_min_latency'] = min
    _statistics['network_avg_latency'] = avg
    _statistics['network_max_latency'] = max

def _get_statistics():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    _get_cpu_info()
    _get_mem_info()
    _get_disk_usage()
    _get_netork_info()

    if not os.path.exists(_file_path):
        f = open(_file_path, "w+")
        f.write(_header_line)
        f.close()

    f = open(_file_path, "a+")
    f.write('\n')
    f.write(
        f"{dt_string}, "
        f"{_statistics['physical_and_logical_cpu_count']}, "
        f"{_statistics['cpu_load']}, "
        f"{_statistics['physical_total_mem']}, "
        f"{_statistics['physical_used_mem']}, "
        f"{_statistics['physical_free_mem']}, "
        f"{_statistics['physical_shared_mem']}, "
        f"{_statistics['physical_buff_cached_available']}, "
        f"{_statistics['swap_total_mem']}, "
        f"{_statistics['swap_used_mem']}, "
        f"{_statistics['swap_free_mem']}, "
        f"{_statistics['swap_buff_cached_available']}, "
        f"{_statistics['total_disk']}, "
        f"{_statistics['used_disk']}, "
        f"{_statistics['free_disk']}, "
        f"{_statistics['network_min_latency']}, "
        f"{_statistics['network_avg_latency']}, "
        f"{_statistics['network_max_latency']}"
    )

if __name__ == "__main__":
    _get_statistics()
