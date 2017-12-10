import psycopg2
import config


class LockError(Exception):
    pass


def set_lock(strict=True):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=config.CONNECTION['USER'],
                           host='localhost',
                           password=config.CONNECTION['PASSWORD'])
    con.autocommit = False
    cur = con.cursor()

    cur.execute("""
          SELECT locks.locked 
          FROM locks WHERE id=1 
          FOR UPDATE
          """)
    if cur.fetchone()[0] and strict:
        raise LockError('Lock was True when set_lock was called')
    else:
        cur.execute("""
                  UPDATE locks 
                  SET locked='True'
                  WHERE id=1 
                  """)
        con.commit()


def release_lock(strict=True):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=config.CONNECTION['USER'],
                           host='localhost',
                           password=config.CONNECTION['PASSWORD'])
    con.autocommit = False
    cur = con.cursor()

    cur.execute("""
          SELECT locks.locked 
          FROM locks WHERE id=1 
          FOR UPDATE
          """)
    if not cur.fetchone()[0] and strict:
        raise LockError('Lock was False when release_lock was called')

    cur.execute("""
              UPDATE locks 
              SET locked='False'
              WHERE id=1 
              """)
    con.commit()