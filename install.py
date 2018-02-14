import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
import logging.handlers
import config


def create_db(user_name, password):

    # check if database doesn't already exists
    try:
        con = psycopg2.connect(dbname='postgres',
                               user=user_name,
                               host='localhost',
                               password=password)

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

        cur = con.cursor()
        cur.execute("CREATE DATABASE payoutscript_administration")
    except psycopg2.ProgrammingError:
        return


def create_table_locks(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS locks (
                       id SERIAL PRIMARY KEY,
                       locked BOOLEAN);""")


def create_table_delegate(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS delegate (
                       id SERIAL PRIMARY KEY,
                       address VARCHAR(50),
                       reward BIGINT);""")


def grant_privileges(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()
    cur.execute("""GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {};""".format(config.CONNECTION['USER']))


def create_empty_lock(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()
    cur.execute("""INSERT INTO 
                   locks 
                   VALUES (1, FALSE)
                   ON CONFLICT DO NOTHING;""")


def create_delegate_entry(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()
    cur.execute("""INSERT INTO delegate (id, address, reward)
                   VALUES (1, '{}', 0)
                   ON CONFLICT DO NOTHING;;""".format(config.DELEGATE['ADDRESS']))


def create_table_users_payouts(user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users_payouts (
                       address VARCHAR(50) PRIMARY KEY,
                       payout BIGINT,
                       last_payout BIGINT);""")


if __name__ == '__main__':
    # Initialize logging
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(config.LOGGING['LOGDIR'],
                                                   encoding='utf-8',
                                                   maxBytes=10 * 1024 * 1024,
                                                   backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(config.LOGGING['LOGGING_LEVEL'])

    user_name = input('Please provide a psql user eligble to create a database:  ')
    password = input('Please provide the password of psql user "{}": '.format(user_name))

    print('Creating database')
    create_db(user_name, password)
    print('Success')
    print('creating tables')
    create_table_locks(user_name, password)
    create_table_delegate(user_name, password)
    create_table_users_payouts(user_name, password)
    print('Success')
    print('granting privileges')
    grant_privileges(user_name, password)
    print('success')
    print('creating lock')
    create_empty_lock(user_name, password)
    print('success')
    print('creating delegate entry')
    create_delegate_entry(user_name, password)
    print('success')
