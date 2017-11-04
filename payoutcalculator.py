import arkdbtools.dbtools as ark

import logging.handlers
import config
import acidfile
import pickle

'''We'll use the same RotatingFileHandler as arkdbtools. However in production I recommend
using https://sentry.io/'''

DELEGATE_ADDRESS = 'AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE'
DELEGATE_PUBKEY = '0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a'


def main():
    # logger.info('setting connection')
    ark.set_connection(
        host='localhost',
        database='ark_mainnet',
        user='ark',
        password=None)

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
            logger.info(i, payouts[i])

    stamp = ark.utils.timestamp(forfilename=True)
    logger.info('writing %s/%s*', config.PAYOUTDIR, stamp)
    nfiles = 0

    for address in payouts:
        nfiles += 1
        savefile = '%s/%s-%s' % (config.PAYOUTDIR, stamp, address)
        data = [address, payouts[address]]
        logger.debug('data for voter payment file %s: %s', savefile, str(data))
        with acidfile.ACIDWriteFile(savefile) as outfile:
            pickle.dump(data, outfile)

    logger.info('%d files written', nfiles)
    logger.info('finished')


if __name__ == '__main__':
    # Initialize logging
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(config.LOGGING['LOG_DIR'],
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
        logger.fatal('caught exception in payoutcalculator: {}'.format(e))
