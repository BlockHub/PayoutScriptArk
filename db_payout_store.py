import psycopg2
from plugandplay import connect, set_params, calculate, format_payments
from arkdbtools.utils import arkt_to_unixt
from arkdbtools.config import ARK
import config
import logging

logger = logging.getLogger(__name__)


def store(payouts, user_name, password, raw_payouts):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()

    for i in raw_payouts:
        timestamp = arkt_to_unixt(raw_payouts[i]['last_payout'])
        share = raw_payouts[i]['share'] * config.SENDER_SETTINGS['DEFAULT_SHARE']
        if not config.SENDER_SETTINGS['COVER_TX_FEES']:
            share -= 0.1*ARK
        cur.execute(
            """
            INSERT
            INTO
            users_payouts(address, payout, last_payout)
            VALUES('{address}', {payout}, ({timestamp}))
            ON CONFLICT(address)
            DO UPDATE
            SET
                payout = {payout},
                last_payout = {timestamp}
            
            WHERE users_payouts.address = '{address}' ;   
            """.format(
                address=i,
                payout=share,
                timestamp=timestamp,
                )
        )


if __name__ == "__main__":
    print('connecting')
    connect()
    print('setting params')
    set_params()
    print('calculating')
    payouts, timestamp = calculate()
    print('formatting')
    formatted_payments = format_payments(payouts, timestamp)
    print('saving')
    store(formatted_payments, config.username, config.password, payouts)



