import os
from ast import literal_eval


def parse_env_info():
    ENV_PROCESS_INFO = os.environ.get('PROCESS_LOG_ARGS')
    # ENV_PROCESS_INFO = ("DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;DATABASE=Test0;DROP_ON_ITER=True;"
    #                     "CSV_PATH=C:\CodeTesting\ProcessReaderCSVOutput;OUTPUT_CSV=True;"
    #                     "FILTERS={};SLEEP_SEC=20")
    info_lst = ENV_PROCESS_INFO.split(';')
    info = {}
    for arg in info_lst:
        key, value = arg.split('=')
        info[key.strip()] = value.strip()

    info['DROP_ON_ITER'] = info['DROP_ON_ITER'] == 'True'
    info['OUTPUT_CSV'] = info['OUTPUT_CSV'] == 'True'
    info['SLEEP_SEC'] = int(info['SLEEP_SEC'])
    info['FILTERS'] = literal_eval(info['FILTERS'])

    return info
