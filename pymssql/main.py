import pyodbc
import argparse as ap
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

def argparser():
    """コマンドライン引数の受け取るための関数
    parserに加えられる引数:
        'input csv'           : 登録用csvファイル
    
    オプション:
        [初期化]
        '-i', '--init' : データベース初期化
        [登録]
        '-r', '--regist' : 指定csvファイルをデータベース登録
        [検索]
        '-s','--search': 登録済みテーブルを検索
            [詳細設定]
            '-a','--address': 検索する都道府県をローマ字で指定
            '-o','--output': csvファイルを出力
        
    Args:
    returns:
        parser.parse_args()   :
    """
    parser = ap.ArgumentParser()

    parser.add_argument("-r","--regist",type=str,
                        help='Regist from input csv')

    parser.add_argument("-a","--address",type=str,
                        help='Select address(Rome)')

    parser.add_argument("-o","--output",type=str,
                        help='output csv')

    parser.add_argument('-i', '--init',
                        default=False,
                        action='store_true',
                        help='initialize database')
    parser.add_argument('-s','--search',
                        default=False,
                        action='store_true',
                        help='search from regist table')
    parser.add_argument('-q','--query',
                        default=False,
                        action='store_true',
                        help='show sql query')


    
    args = parser.parse_args()
    return args


def main():
    server = '127.0.0.1'
    database = 'PersonalInfo' #データベース名
    username = 'SA'
    password = 'Jmiri2020' #サーバーに設定したパスワード
    conn = connection(server, database, username, password)
    args = argparser()
    if args.init:
        if input('Please password \n') == 'INITIALIZE':
            initialize(conn, database)
        else:
            logger.error('Password is incorrect')
            exit()
    elif args.regist:
        input_csv = args.regist
        regist(conn, input_csv)
    elif args.search:
        select_tables(conn, 'BaseInfo', args)
    logger.info('finished')
    conn.close()


if __name__ == "__main__":
    main()