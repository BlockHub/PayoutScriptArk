import arkdbtools.dbtools as ark
import arkdbtools.config as info
import logging.handlers
import config
import utils
from arky import api, core


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
        secret=config.DELEGATE['SECRET'],
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
                    continue

            else:
                res.update({payout: amount})

    try:
        for x in config.HARD_EXCEPTIONS:
            if config.HARD_EXCEPTIONS[x] <= payouts[x]['share'] \
            and payouts[x]['last_payout'] < timestamp - config.SENDER_SETTINGS['WAIT_TIME']:

                amount = config.HARD_EXCEPTIONS[x] + fees
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

    return res


def transmit_payments(payouts):
    failed_amount = 0
    api.use(network='ark')
    for ark_address in payouts:

        tx = core.Transaction(
            amount=payouts[ark_address],
            recipientId=ark_address,
            vendorField=config.SENDER_SETTINGS['PERSONAL_MESSAGE'])

        if config.DELEGATE['SECOND_SECRET']:
            tx.sign(secret=config.DELEGATE['SECRET'],
                    secondSecret=config.DELEGATE['SECOND_SECRET'])
        else:
            tx.sign(secret=config.DELEGATE['SECRET'])

        tx.serialize()
        res = api.sendTx(
           tx=tx,
           url_base=config.IP,
           secret=config.DELEGATE['SECRET'],
           secondSecret=config.DELEGATE['SECOND_SECRET']
                   )
        if not res['success']:
            logger.warning('{}'.format(res))



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
        formatted_payouts = format_payments(
            payouts=rawpayouts,
            timestamp=timestamp
        )
        if config.PAYOUTCALCULATOR_TEST:
            logger.info('FORMATTED PAYMENTS')
            for i in formatted_payouts:
                logger.info('{} ---- {}'.format(i, formatted_payouts[i]/info.ARK))
        else:
            logger.info('transmitting payouts')
            transmit_payments(payouts=formatted_payouts)

        if config.USE_LOCKS:
            utils.release_lock()

    except Exception:
        logger.exception('caught exception in plugandplay')
        raise