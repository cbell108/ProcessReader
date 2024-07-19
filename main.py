import processInfoRead
import databaseConnecter
import envVar

import time
import pandas as pd
import win32evtlog
import win32evtlogutil
from classes import classDef as clsdef
from os.path import join
from datetime import datetime
from sqlalchemy import exc

cd = clsdef.DBConnector()


# PYWIN32 for logging errors

# Calls DatabaseConnecter module, passes arguments to specify connection operations
def main_dbinsert_lst(lib, DRIVER, SERVER, DATABASE):
    return databaseConnecter.dbcon_start(lib=lib  # 'sqlalchemy' or 'pyodbc'
                                         , DRIVER=DRIVER
                                         , SERVER=SERVER
                                         , DATABASE=DATABASE
                                         )


def log_error(err_id, msg):
    if err_id == 0:
        evt_type = win32evtlog.EVENTLOG_SUCCESS
    else:
        evt_type = win32evtlog.EVENTLOG_ERROR_TYPE

    win32evtlogutil.ReportEvent(
        appName="ProcessReader",
        eventID=err_id,
        eventCategory=0,
        eventType=evt_type,
        strings=["Error message", msg],
        data=None,
        sid=None
    )


# Retrieves processes using ProcessInfoRead module, passes to DatabaseConnecter
if __name__ == "__main__":
    env_info = envVar.parse_env_info()

    DRIVER = env_info['DRIVER']
    SERVER = env_info['SERVER']
    DATABASE = env_info['DATABASE']
    drop_tbl = env_info['DROP_ON_ITER']
    csv_path = env_info['CSV_PATH']
    output_csv = env_info['OUTPUT_CSV']
    sleep_sec = env_info['SLEEP_SEC']
    filters = env_info['FILTERS']

    # Process Loop
    engine = None
    try:
        engine = main_dbinsert_lst(cd.SQLALCHEMY, DRIVER, SERVER, DATABASE)
        while True:
            # Get processes
            cur_processes_dct = processInfoRead.get_process_info(filters)
            process_df = pd.DataFrame(cur_processes_dct)
            cur_date = datetime.now()
            process_df['InsertTime'] = cur_date

            if output_csv:
                csv_filename = "ProcessLog_" + cur_date.strftime('%Y%m%d_%H%M%S') + ".csv"
                process_df.to_csv(join(csv_path, csv_filename), index=False, header=True)

            if drop_tbl:
                databaseConnecter.exec_stored_proc_sqlalchemy(engine, True)

            databaseConnecter.insert_sqlalchemy(engine, process_df)
            time.sleep(sleep_sec)
    except SystemExit as e:
        log_error(0, "Process termination error:" + str(e))
    except (FileNotFoundError, PermissionError) as e:
        log_error(1, "CSV creation error:" + str(e))
    except exc.SQLAlchemyError as e:
        log_error(2, "SQLAlchemy error:" + str(e))
    except Exception as e:
        log_error(3, "Uncaught error:" + str(e))
    finally:
        if engine:
            engine.dispose()
