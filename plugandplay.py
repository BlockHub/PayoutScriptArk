import arkdbtools.dbtools as ark
import arkdbtools.config as info
import logging.handlers
import config
import datetime
import arky
'''
We'll use the same RotatingFileHandler as arkdbtools. However in production I recommend
using https://sentry.io/
'''


def main():
    # logger.info('setting connection')
    ark.set_connection(
        host=config.CONNECTION['HOST'],
        database=config.CONNECTION['DATABASE'],
        user=config.CONNECTION['USER'],
        password=config.CONNECTION['PASSWORD'])

    # check if node is at reasonable height. 51 means you are at maximum
    # 2 forged blocks behind.
    logger.info('checking node')
    if config.PAYOUTCALCULATOR_TEST:
        logger.info('--TESTMODE ON-- Node status: {}. Continuing main'.format(ark.Node.check_node(51)))
    else:
        if not ark.Node.check_node(51):
            logger.fatal('NodeDbError, node was more than 51 blocks behind')
            raise ark.NodeDbError('NodeDbError, node was more than 51 blocks behind')
        logger.info('Node was within 51 blocks of the network')

    ark.set_delegate(
        address= config.DELEGATE['ADDRESS'],
        pubkey=  config.DELEGATE['PUBKEY'],
        secret=  config.DELEGATE['PASSPHRASE'],
    )
    logger.debug('setting delegate: {0}, {1}'.format(config.DELEGATE['ADDRESS'], config.DELEGATE['PUBKEY']))

    ark.set_calculation(
        blacklist=config.BLACKLIST
    )

    print('starting calculation')
    payouts, timestamp = ark.Delegate.trueshare(start_block=config.CALCULATION_SETTINGS['STARTBLOCK_CALCULATION'])

    if config.PAYOUTCALCULATOR_TEST:
        for i in payouts:
            logger.info('{0} ----  {1}(share) ---- {2}(balance)'.format(i, payouts[i]['share']/info.ARK, payouts[i]['balance']/info.ARK))

    logger.info('starting transmitting payouts')
    delegate_share = 0

    print('starting transmission')

    if config.SENDER_SETTINGS['COVER_TX_FEES']:
        fees = info.TX_FEE
    else:
        fees = 0
    ark.set_sender(payoutsender_test=config.PAYOUTCALCULATOR_TEST)
    current_day = datetime.datetime.today().weekday()

    # lets deal with the exceptions first:
    try:
        for x in config.HARD_EXCEPTIONS:
            if config.HARD_EXCEPTIONS[x] <= payouts[x]['share'] \
            and config.SENDER_SETTINGS['DAY_WEEKLY_PAYOUT'] == current_day \
            and payouts[x]['last_payout'] < timestamp - config.SENDER_SETTINGS['WAIT_TIME']:
                try:
                    ark.Core.send(
                        address=x,
                        amount=config.HARD_EXCEPTIONS[x],
                        smartbridge=config.SENDER_SETTINGS['PERSONAL_MESSAGE'],
                        secret=config.DELEGATE['PASSPHRASE'])
                    delegate_share += (payouts[x]['share'] - config.HARD_EXCEPTIONS[x] + fees)
                except Exception:
                    logger.exception('failed a HARD EXCEPTION transaction')

    except Exception:
        logger.exception('failed transmitting hard exception payments')

    for payout in payouts:

        amount = (payouts[payout]['share'] * config.SENDER_SETTINGS['DEFAULT_SHARE']) + fees

        if amount > config.SENDER_SETTINGS['MIN_PAYOUT_BALANCE'] \
        and config.SENDER_SETTINGS['DAY_WEEKLY_PAYOUT'] == current_day \
        and payouts[payout]['last_payout'] < timestamp - config.SENDER_SETTINGS['WAIT_TIME']:

            if config.SENDER_SETTINGS['REQUIRE_CURRENT_VOTER']:
                if payouts[payout]['status']:
                    try:
                        res = ark.Core.send(
                            address=payout,
                            amount=amount,
                            smartbridge=config.SENDER_SETTINGS['PERSONAL_MESSAGE'],
                            secret=config.DELEGATE['PASSPHRASE'])
                        delegate_share += payouts[payout]['share'] - amount
                        logger.debug(res)
                    except Exception:
                        logger.exception('failed transaction:')
                    continue

            else:
                try:
                    res = ark.Core.send(
                        address=payout,
                        amount=amount,
                        smartbridge=config.SENDER_SETTINGS['PERSONAL_MESSAGE'],
                        secret=config.DELEGATE['PASSPHRASE'])
                    delegate_share += payouts[payout]['share'] - amount
                    logger.debug(res)
                except Exception:
                    logger.exception('failed transaction:')

    # sending payouts to the rewardwallet
    ark.Core.send(
        address=config.DELEGATE['REWARDWALLET'],
        amount=delegate_share,
        secret=config.DELEGATE['PASSPHRASE'])


if __name__ == '__main__':
    # Initialize logging
    print('initializing logging')
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
        main()
    except Exception as e:
        pass
        logger.fatal('caught exception in plugandplay: {}'.format(e))