import pyodbc
from pymssql.mylogger import logger
from pymssql.function import (initialize, 
                              create_meta_table,
                              create_base_info_table,
                              create_contact_info_table,
                              create_address_info_table,
                              check_table_exists,
                              delete_tables,
                              regist,
                              set_db_dict,
                              insert,
                              str_editor,
                              select_tables,
                              select_tracks)


def connection(server, database, username, password):
    conn = pyodbc.connect(
                          'DRIVER={ODBC Driver 17 for SQL Server}; \
                           SERVER='+server+'; \
                           DATABASE='+database+'; \
                           UID='+username+'; \
                           PWD='+ password
    )
    return conn


def main():
    server = '127.0.0.1'
    database = 'PersonalInfo' #データベース名
    username = 'SA'
    password = 'Jmiri2020' #サーバーに設定したパスワード
    conn = connection(server, database, username, password)
    initialize(conn, database)
    #regist(conn, './data/personal_infomation.csv')
    regist(conn, './data/test_data.csv')
    select_tables(conn, 'BaseInfo')
    logger.info('finished')
    conn.close()


if __name__ == "__main__":
    main()