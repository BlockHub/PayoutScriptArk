import arkdbtools.dbtools as ark
import arkdbtools.config as info
import logging.handlers
import config
import utils
import psycopg2

'''
We'll use the same RotatingFileHandler as arkdbtools. However in production I recommend
using https://sentry.io/
'''


def connect():
    ark.set_connection(
        host=config.CONNECTION['HOST'],
        database=config.CONNECTION['DATABASE'],
        user=config.CONNECTION['USER'],
        password=config.CONNECTION['PASSWORD'])


def set_params():
    ark.set_delegate(
        address=config.DELEGATE['ADDRESS'],
        pubkey=config.DELEGATE['PUBKEY'],
        secret=config.DELEGATE['PASSPHRASE'],
    )
    logger.info('setting delegate: {0}, {1}'.format(config.DELEGATE['ADDRESS'], config.DELEGATE['PUBKEY']))

    ark.set_calculation(
        blacklist=config.BLACKLIST
    )
    ark.set_sender(payoutsender_test=config.PAYOUTSENDER_TEST)


def check_node_height():
    # check if node is at reasonable height. 51 means you are at maximum
    # 2 forged blocks behind.
    if config.PAYOUTCALCULATOR_TEST:
        logger.info('--TESTMODE ON-- Node status: NOT CHECKED. Continuing main')
    else:
        if not ark.Node.check_node(51):
            logger.fatal('NodeDbError, node was more than 51 blocks behind')
            raise ark.NodeDbError('NodeDbError, node was more than 51 blocks behind')
        logger.info('Node was within 51 blocks of the network')


def calculate():
    payouts, timestamp = ark.Delegate.trueshare(start_block=config.CALCULATION_SETTINGS['STARTBLOCK_CALCULATION'])

    if config.PAYOUTCALCULATOR_TEST:
        logger.info('TRUE PAYMENTS')
        for i in payouts:
            logger.info('{0} ----  {1}(share) ---- {2}(balance)'.format(i, payouts[i]['share']/info.ARK, payouts[i]['balance']/info.ARK))
    return payouts, timestamp


def format_payments(payouts, timestamp):
    delegate_share = 0
    res = {}

    # delegates substract fees from the amount you are sending. So if you transmit 1 Ark, the receiver will get 0.9 Ark
    if config.SENDER_SETTINGS['COVER_TX_FEES']:
        fees = 0
    else:
        fees = - info.TX_FEE

    for payout in payouts:

        amount = (payouts[payout]['share'] * config.SENDER_SETTINGS['DEFAULT_SHARE']) + fees

        if amount >= config.SENDER_SETTINGS['MIN_PAYOUT_BALANCE'] \
        and payouts[payout]['last_payout'] < timestamp - config.SENDER_SETTINGS['WAIT_TIME']:

            if config.SENDER_SETTINGS['REQUIRE_CURRENT_VOTER']:
                if payouts[payout]['status']:
                    res.update({payout: amount})
                    delegate_share += payouts[payout]['share'] - amount

                    continue

            else:
                res.update({payout: amount})
                delegate_share += payouts[payout]['share'] - amount
                logger.debug(res)


    try:
        for x in config.HARD_EXCEPTIONS:
            if config.HARD_EXCEPTIONS[x] <= payouts[x]['share'] \
            and payouts[x]['last_payout'] < timestamp - config.SENDER_SETTINGS['WAIT_TIME']:

                amount = config.HARD_EXCEPTIONS[x] + fees
                delegate_share += (payouts[x]['share'] - amount)
                res.update({
                    config.HARD_EXCEPTIONS[x]: amount,
                })
    except TypeError:
        logger.exception('failed in setting payout for hard exceptions')

    try:
        for address in config.DARKLIST:
            res.pop(address, None)
    except TypeError:
        pass

    return res, delegate_share


def transmit_payments(payouts):
    delegate_share = 0
    failed_amount = 0
    for ark_address in payouts:
        try:
            ark.Core.send(
                address=ark_address,
                amount=payouts[ark_address],
                secret=config.DELEGATE['PASSPHRASE'],
                smartbridge=config.SENDER_SETTINGS['PERSONAL_MESSAGE'],
            )
            delegate_share += payouts[ark_address]
        except ark.ApiError:
            logger.warning('APIerror, failed a transaction')
            failed_amount += payouts[ark_address]
    return delegate_share, failed_amount


def get_delegate_share():
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=config.CONNECTION['USER'],
                           host='localhost',
                           password=config.CONNECTION['PASSWORD'])

    cur = con.cursor()

    cur.execute("""
              SELECT delegate.reward 
              FROM delegate WHERE id=1 
              """)
    return cur.fetchone()[0]


def save_delegate_share(total_share):
    con = psycopg2.connect(dbname='payoutscript_administration',
                           user=config.CONNECTION['USER'],
                           host='localhost',
                           password=config.CONNECTION['PASSWORD'])

    cur = con.cursor()

    cur.execute("""
                UPDATE delegate 
                SET reward={}
                WHERE id=1""".format(total_share))
    con.commit()


def handle_delegate_reward(amount, current_timestamp):
    reward = get_delegate_share() + amount
    last_payout = ark.Address.payout(config.DELEGATE['REWARDWALLET'])[-1].timestamp

    if last_payout < current_timestamp - config.SENDER_SETTINGS['WAIT_TIME_REWARD'] and reward > info.TX_FEE:
        res = ark.Core.send(
                address=config.DELEGATE['REWARDWALLET'],
                amount=reward,
                secret=config.DELEGATE['PASSPHRASE'],
                smartbridge=config.DELEGATE['REWARD_SMARTBRIDGE'])
        if res:
            save_delegate_share(0)
        else:
            logger.warning('unable to transmit delegate reward. Stored it in the db.')
            save_delegate_share(reward)
    else:
        save_delegate_share(reward)


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

    if config.PAYOUTCALCULATOR_TEST:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(config.LOGGING['LOGGING_LEVEL'])

    # Protect the entire run in a try block so we get postmortem info if
    # applicable.
    try:
        if config.USE_LOCKS:
            utils.set_lock()
        logger.info('connecting to DB')
        connect()
        logger.info('setting parameters')
        set_params()
        logger.info('checking height')
        check_node_height()
        logger.info('calculating payouts')
        rawpayouts, timestamp = calculate()
        logger.info('formatting payouts')
        formatted_payouts, true_delegate_share = format_payments(
            payouts=rawpayouts,
            timestamp=timestamp
        )
        if config.PAYOUTCALCULATOR_TEST:
            logger.info('FORMATTED PAYMENTS')
            for i in formatted_payouts:
                logger.info('{} ---- {}'.format(i, formatted_payouts[i]/info.ARK))
            logger.info('DELEGATESHARE: {}'.format(true_delegate_share))
        else:
            logger.info('transmitting payouts')
            delegate_share, failed_amount = transmit_payments(
                                payouts=formatted_payouts
                                )
            logger.info('sending delegate share: {}'.format(delegate_share))
            handle_delegate_reward(delegate_share, current_timestamp=timestamp)
        if config.USE_LOCKS:
            utils.release_lock()
    except Exception:
        logger.exception('caught exception in plugandplay')
        raise