This program is used to read information about currently running processes (like Task Manager), and periodically insert this data into a database table or output as a .csv file.

1) Reads parameters from environment variable 'PROCESS_LOG_ARGS'
* Parameters are DRIVER, SERVER, DATABASE, DROP_ON_ITER, CSV_PATH, OUTPUT_CSV, FILTERS, SLEEP_SEC
* Each parameter and its value are delimited by a semicolon ';'
* E.g.: DRIVER=ODBC Driver 17 for SQL Server;SERVER=localhost;DATABASE=Test0;DROP_ON_ITER=True;CSV_PATH=C:\CodeTesting\ProcessReaderCSVOutput;OUTPUT_CSV=True;FILTERS={'Name':['python.exe', 'chrome.exe']};SLEEP_SEC=20

2) Process values to filter by (exact match, at least 1 from each selected filter category):
* CreateTime, PID, PPID, Name, User, Status

3) Uses stored procedure 'usp_CreateOrTruncate_ProcessLogTable' to create table 'ProcessLog' if object does not exist
* Env variable 'DROP_ON_ITER' is passed as argument to trunicate table every iteration.
