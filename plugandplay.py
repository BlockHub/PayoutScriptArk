import arkdbtools.dbtools as ark
import arkdbtools.config as info
import logging.handlers
import config
import pickle

'''We'll use the same RotatingFileHandler as arkdbtools. However in production I recommend
using https://sentry.io/'''

DELEGATE_ADDRESS = 'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE'
DELEGATE_PUBKEY = '0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a'


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
            # logger.fatal('NodeDbError, node was more than 51 blocks behind')
            raise ark.NodeDbError('NodeDbError, node was more than 51 blocks behind')
        logger.info('Node was within 51 blocks of the network')


    logger.debug('setting delegate: {0}, {1}'.format(DELEGATE_ADDRESS, DELEGATE_PUBKEY))

    ark.set_delegate(
        address= DELEGATE_ADDRESS,
        pubkey=  DELEGATE_PUBKEY
    )

    ark.set_calculation()

    payouts, timestamp = ark.Delegate.share()

    if config.PAYOUTCALCULATOR_TEST:
        for i in payouts:
            logger.info('{0} ----  {1}(share) ---- {2}(balance)'.format(i, payouts[i]['share']/info.ARK, payouts[i]['balance']/info.ARK))

    ark.set_sender(
        default_share=config.SENDER_SETTINGS['DEFAULT_SHARE'],
        cover_fees=config.SENDER_SETTINGS['COVER_TX_FEES'],
        share_percentage_exceptions=config.SHARE_EXCEPTIONS,
        timestamp_brackets=config.SENDER_SETTINGS['TIMESTAMP_BRACKETS'],
        min_payout_daily=config.SENDER_SETTINGS['MIN_PAYOUT_BALANCE_DAILY'],
        min_payout_weekly=config.SENDER_SETTINGS['MIN_PAYOUT_BALANCE_WEEKLY'],
        min_payout_monthly=config.SENDER_SETTINGS['MIN_PAYOUT_BALANCE_MONTHLY'],
        day_weekly_payout=config.SENDER_SETTINGS['DAY_WEEKLY_PAYOUT'],
        day_monthly_payout=config.SENDER_SETTINGS['DAY_MONTHLY_PAYOUT'],
        payoutsender_test=config.PAYOUTCALCULATOR_TEST,
        sender_exception=config.HARD_EXCEPTIONS,
        wait_time_day=config.SENDER_SETTINGS['WAIT_TIME_DAILY'],
        wait_time_week=config.SENDER_SETTINGS['WAIT_TIME_DAILY'],
        wait_time_month=config.SENDER_SETTINGS['WAIT_TIME_DAILY'],
    )
    failed_payouts = 0
    successful_payouts = 0
    stored_payouts = 0
    logger.info('starting transmitting payouts')
    delegate_share = 0
    for payout in payouts:
        data = payout, payouts[payout]
        try:
            result, delegate_reward, amount = ark.Core.payoutsender(data, calculation_timestamp=timestamp)
            delegate_share += delegate_reward

        except ark.TxParameterError:
            stored_payouts += 1
            logger.info('Txparametererror, stored payout')
        if result:
            successful_payouts += 1
            logger.info('sent {0} to {1}, delegate_reward: {2}'.format(amount, payout, delegate_reward))
        else:
            failed_payouts += 1
            logger.fatal('payout failed for {0}, response: {1}'.format(payout, result))

    ark.Core.send(config.DELEGATE['REWARDWALLET'], delegate_share)
    logger.info('sent {0} to delegate: {1}'.format(delegate_share, config.DELEGATE['REWARDWALLET']))

    logger.info('Successful payouts: {0}, failed payouts: {1}'.format(successful_payouts, failed_payouts))
    logger.info(('failed payouts: {}'.format(failed_payouts)))
    logger.info('stored payouts: {}'.format(stored_payouts))
    logger.info('delegate_share: {}'.format(delegate_share))


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
        main()
    except Exception as e:
        pass
        logger.fatal('caught exception in plugandplay: {}'.format(e))