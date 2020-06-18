from pymssql.mylogger import logger

########################
#    DELETE & CREATE   #
########################

def initialize(conn, db_name):
    table_name_list = ['meta','BaseInfo', 'ContactInfo', 'AdressInfo']
    if all([check_table_exists(conn, t) for t in table_name_list]):
        delete_tables(conn, table_name_list)
    create_meta_table(conn)
    create_contact_info_table(conn)
    create_address_info_table(conn)
    create_base_info_table(conn)
    print('Initialize tables done!!')

def create_table(conn, table_name, name_type_dict):
    cur = conn.cursor()
    bodylist = []
    for name in name_type_dict.keys():
        bodylist.append(' ' + name + ' ' + name_type_dict[name])
    query1 = "IF OBJECT_ID('{0}') IS NULL CREATE TABLE {0} (".format(table_name)
    body = ','.join(bodylist)
    query2 = ");"
    query = query1 + body + query2
    #print(query)
    cur.execute(query)
    conn.commit()

def create_meta_table(conn):
    table_name = "Meta"
    ig = 'INT'
    pk = ' IDENTITY'
    date = 'DATE'
    null = ' NOT NULL'
    bit = 'BIT'
    name_type_dict = {'sample_id': ig + pk,
                      'update_day': date + null,
                      'delete_flag': bit + null
                      }
    create_table(conn, table_name, name_type_dict)


def create_base_info_table(conn):
    table_name = "BaseInfo"
    ig = 'INT'
    vc1 = 'NVARCHAR(1)'
    vc2 = 'NVARCHAR(2)'
    vc30 = 'NVARCHAR(30)'
    pk = ' IDENTITY'
    date = 'date'
    null = ' NOT NULL'
    name_type_dict = {'sample_id': ig + pk,
                      'name': vc30 + null,
                      'name_kata': vc30 + null,
                      'name_rome': vc30 + null,
                      'sex': vc1 + null,
                      'birthday': date + null,
                      'age': ig + null,
                      'blood_type': vc2 + null}
    create_table(conn, table_name, name_type_dict)


def create_contact_info_table(conn):
    table_name = "ContactInfo"
    ig = 'INT'
    big = 'bigint'
    vc = 'NVARCHAR(64)'
    pk = ' IDENTITY'
    name_type_dict = {'sample_id': ig + pk,
                      'phone_number': big,
                      'cell_phone_number': big,
                      'mail_address': vc}
    create_table(conn, table_name, name_type_dict)


def create_address_info_table(conn):
    table_name = "AdressInfo"
    ig = 'INT'
    vc = 'NVARCHAR(100)'
    pk = ' IDENTITY'
    name_type_dict = {'sample_id': ig + pk,
                      'zip': ig,
                      'address': vc,
                      'address_kata': vc,
                      'address_rome': vc
                    }
    create_table(conn, table_name, name_type_dict)

def check_table_exists(conn, table_name):
    cur = conn.cursor()
    query = "select name from sys.objects where (type = 'U' AND object_id = object_id( '{}'));".format(table_name)
    cur.execute(query)
    result = cur.fetchone()
    if result:
        return True
    else:
        False

def delete_tables(conn, table_name_list):
    cur = conn.cursor()
    query = 'DROP TABLE IF EXISTS {}'.format(
                ', '.join(table_name_list)
            )
    cur.execute(query)


#################
#    register   #
#################


def regist(conn, inputfile):
    logger.info('Mode: regist')
    with open(inputfile, 'r')as rf:
        # 1行目のheaderはいらない
        line = rf.readline()
        line = rf.readline()
        while line:
            persodic = set_db_dict(line)
            insert(conn, 'Meta', ['update_day','delete_flag'], ['GETDATE()', 0])
            insert(conn, 'BaseInfo', persodic['base'].keys(), persodic['base'].values())
            insert(conn, 'ContactInfo', persodic['contact'].keys(), persodic['contact'].values())
            insert(conn, 'AdressInfo', persodic['adress'].keys(), persodic['adress'].values())
            line = rf.readline()


def set_db_dict(line):
    persodic = {}
    persodic['base'] = {}
    persodic['contact'] = {}
    persodic['adress'] = {}
    line = line.split(',')
    persodic['base']['name'] = line[1]
    persodic['base']['name_kata'] = line[2]
    persodic['base']['name_rome'] = line[3]
    persodic['base']['sex'] = line[4]
    persodic['contact']['phone_number'] = int(line[5])
    persodic['contact']['cell_phone_number'] = int(line[6]) if line[6] else ''
    persodic['contact']['mail_address'] = line[7]
    persodic['adress']['zip'] = int(line[8].replace('-',''))
    persodic['adress']['address'] = ''.join(line[9:13])
    persodic['adress']['address_kata'] = ''.join(line[14:18])
    persodic['adress']['address_rome'] = ''.join(line[19:23])
    persodic['base']['birthday'] = line[24].replace('/','-')
    persodic['base']['age'] = int(line[25])
    persodic['base']['blood_type'] = line[26].rstrip('\n')
    #print(persodic)
    return persodic


def insert(conn, table_name, column_list, value_list):
    cur = conn.cursor()
    value_list = [str_editor(s) for s in value_list]
    query1 = "INSERT INTO " + table_name + " ("
    body = ', '.join(column_list) + ") VALUES (" + ', '.join(value_list) + ");"
    query = query1 + body
    #print(query)
    cur.execute(query)
    conn.commit()


def str_editor(strings):
    if strings == 'GETDATE()':
        return strings
    if type(strings) is str:
        return "'" + strings + "'"
    else:
        return str(strings)


###############
#    select   #
###############


def select_tracks(conn, table_name, flag, column_list, inner_list, condition_list = []):
    cur = conn.cursor()
    columns = ','.join(column_list)
    inner_joins = ' '.join(inner_list) if inner_list else ''
    conditions = ' '.join(condition_list) if inner_list else ''
    query = 'SELECT {} FROM {} {} {}'.format(columns, table_name, inner_joins, conditions)
    if flag:
        logger.info(query)
    rows = cur.execute(query).fetchall()
    outputformat(column_list, rows)
    conn.commit()


def select_tables(conn, table_name, query_flag , address):
    logger.info('Mode: search')
    inner_joins = []
    target_column = ['BaseInfo.sample_id', 'name', 'sex', 'birthday', 'age', 'blood_type',
                    'phone_number', 'cell_phone_number', 'mail_address', 'zip', 'address',
                    'update_day']
    inner_join = 'INNER JOIN ContactInfo ON BaseInfo.sample_id = ContactInfo.sample_id'
    inner_joins.append(inner_join)
    inner_join = 'INNER JOIN AdressInfo ON BaseInfo.sample_id = AdressInfo.sample_id'
    inner_joins.append(inner_join)
    inner_join = 'INNER JOIN Meta ON BaseInfo.sample_id = Meta.sample_id'
    inner_joins.append(inner_join)

    condition_list = []
    if address:
        condition = "WHERE address_rome LIKE '{}%'".format(address)
        condition_list.append(condition)
    select_tracks(conn, table_name, query_flag, target_column, inner_joins, condition_list)


def outputformat(column_list, results):
    column_list[0] = 'sample_id'
    header = '\t'.join(column_list)
    print('\n' + header)
    num = 0
    for row in results:
        result = '\t'.join(map(str, row))
        print(result)
        num += 1
    print('\n({} rows affected)'.format(str(num)))
    