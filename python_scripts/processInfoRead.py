import psutil
from datetime import datetime


# Creates a list of all processes, where data is stored in a dictionary.
# Processes causing AccessDenied errors are skipped.
def get_from_psutil():
    processes = []
    for process in psutil.process_iter():
        try:
            with process.oneshot():
                info = {
                    "CreateTime": datetime.fromtimestamp(process.create_time()),
                    "PID": process.pid,
                    "PPID": process.ppid(),
                    "Name": process.name(),
                    "User": process.username(),  # Throws psutil.AccessDenied
                    "Status": process.status(),
                    # "cpu_times": process.cpu_times(),
                    # "cpu_percent": process.cpu_percent(interval=0),
                    # "memory_percent": process.memory_percent()
                }
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            # print(f"{type(e)} : {e}")
            pass
    return processes


# Skips processes which do not match filters.
# Current implement: must match at least 1 filter in each column where specified
# Need to add filter types: match >=1 any column, comparisons (ex. '> 01:00:00')
def filter_process(arr_proc_dict, filters=None):
    filtered_processes = []
    for proc in arr_proc_dict:
        match_filter = True
        for key, value in filters.items():  # If exact column value not included in filter, flag as false
            if proc[key] not in value:
                match_filter = False
                break

        if match_filter:
            filtered_processes.append(proc)

    return filtered_processes


# Module driver method: calls retrieval and filter methods, creates run_time columns for remaining processes
def get_process_info(filter_params):
    process_info = get_from_psutil()
    if filter_params:
        print("Filtering")
        process_info = filter_process(process_info, filter_params)
    return process_info
