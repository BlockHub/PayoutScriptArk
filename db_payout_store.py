import psycopg2
from plugandplay import connect, set_params, calculate, format_payments
from arkdbtools.utils import arkt_to_unixt
import config


def store(payouts, user_name, password):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=user_name,
                           host='localhost',
                           password=password)
    con.autocommit = True

    cur = con.cursor()

    for i in payouts:
        timestamp = arkt_to_unixt(payouts[i]['last_payout'])


        cur.execute(
            """
            INSERT
            INTO
            users_payouts(address, payout, last_payout)
            VALUES('{address}', {payout}, {timestamp})
            ON CONFLICT(address)
            DO UPDATE
            SET
                payout = {payout};
                last_payout = {timestamp}
            
            WHERE address = '{address}'    
            """.format(
                address=i,
                payout=i['share'],
                timestamp=timestamp,
                )
        )


if __name__ == "__main__":
    connect()
    set_params()
    payouts, timestamp = calculate()
    formatted_payments = format_payments(payouts, timestamp)
    store(formatted_payments, config.username, config.password)



