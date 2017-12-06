import arkdbtools.dbtools as ark
import arkdbtools.config as info
import logging.handlers
import config
import datetime

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


def check_node_height():
    # check if node is at reasonable height. 51 means you are at maximum
    # 2 forged blocks behind.
    if config.PAYOUTCALCULATOR_TEST:
        logger.info('--TESTMODE ON-- Node status: {}. Continuing main'.format(ark.Node.check_node(51)))
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
        fees = info.TX_FEE
    else:
        fees = 0

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
                logger.exception('failed transaction:')


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

    return res, delegate_share


def transmit_payments(payouts):
    current_day = datetime.datetime.today().weekday()
    if config.SENDER_SETTINGS['DAY_WEEKLY_PAYOUT'] == current_day:
        for i in payouts:
            ark.Core.send(
                address=i,
                amount=payouts[i],
                secret=config.DELEGATE['PASSPHRASE'],
                smartbridge=config.SENDER_SETTINGS['PERSONAL_MESSAGE'],
            )


def send_delegate_share(amount):
    # sending payouts to the rewardwallet
    ark.Core.send(
        address=config.DELEGATE['REWARDWALLET'],
        amount=amount,
        secret=config.DELEGATE['PASSPHRASE'])


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
        logger.info('connecting to DB')
        connect()
        logger.info('setting parameters')
        set_params()
        logger.info('checking height')
        check_node_height()
        logger.info('calculating payouts')
        rawpayouts, timestamp = calculate()
        logger.info('formatting payouts')
        formatted_payouts, delegate_share = format_payments(
            payouts=rawpayouts,
            timestamp=timestamp
        )
        if config.PAYOUTCALCULATOR_TEST:
            logger.info('FORMATTED PAYMENTS')
            for i in formatted_payouts:
                logger.info('{} ---- {}'.format(i, formatted_payouts[i]/info.ARK))
            logger.info('DELEGATESHARE: {}'.format(delegate_share))
        else:
            logger.info('transmitting payouts')
            transmit_payments(
                payouts=formatted_payouts
                )
            logger.info('sending delegate share')
            send_delegate_share(
                amount=delegate_share
            )
    except Exception:
        logger.exception('caught exception in plugandplay: {}'.format(e))
        raise