import pyodbc
import sqlalchemy.exc
from sqlalchemy import create_engine, event, text


# From parameters: gets environmental variables, uses sqlalchemy/pyodbc and passes arguments for data
# UID/PWD unimplemented, need security
def dbcon_start(lib='sqlalchemy', DRIVER=None, SERVER=None,
                DATABASE=None, UID=None, PWD=None):
    if lib == 'sqlalchemy':
        if UID and PWD:
            conn_str = f'mssql+pyodbc://{UID}:{PWD}@{SERVER}/{DATABASE}?driver={DRIVER}'
        else:
            conn_str = f'mssql+pyodbc://{SERVER}/{DATABASE}?driver={DRIVER}&trusted_connection=yes'
        return conn_sqlalchemy(conn_str)
    # elif lib == 'pyodbc':
    #     if UID and PWD:
    #         conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};'
    #     else:
    #         conn_str = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    #     return conn_pyodbc(conn_str)


# dbo.usp_test handles table creation
# Creates sqlalchemy connection engine
def conn_sqlalchemy(conn_str):
    engine = create_engine(conn_str)
    exec_stored_proc_sqlalchemy(engine, False)
    return engine


def exec_stored_proc_sqlalchemy(engine, drop_tbl_flag):
    with engine.connect() as conn:
        stmt = text(f"EXEC dbo.usp_CreateOrTruncate_ProcessLogTable @reset=:reset_arg")
        conn.execute(stmt, {'reset_arg': drop_tbl_flag})
        conn.commit()


def insert_sqlalchemy(engine, data):
    with engine.connect() as conn:
        @event.listens_for(engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True

        data.to_sql('ProcessLog', conn, index=False, if_exists="append")
        conn.commit()

#
# # Creates and uses pyodbc connection
# def conn_pyodbc(conn_str, data, table_name, drop_tbl_flag=False):
#     stor_pro = "dbo.usp_CreateOrTruncate_ProcessLogTable"
#
#     conn = pyodbc.connect(conn_str)
#     with conn.cursor() as cursor:
#         cursor.execute(f"EXEC {stor_pro} ?, ?", (table_name, drop_tbl_flag))
#
#         insert_format = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
#         data_tuples = [tuple(row) for row in data.values]
#         cursor.executemany(insert_format, data_tuples)
#
#         conn.commit()
#     conn.close()
