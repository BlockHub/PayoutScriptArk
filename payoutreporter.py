import config
import glob
import logging.handlers
import sys
import arkdbtools.dbtools as ark
import arkdbtools.utils as utils


def main():
    # Report on active payment files
    paymentfiles = sorted(glob.glob(config.PAYOUTDIR + '/*'))
    if len(paymentfiles) == 0:
        logger.info('no payment files to process')
    else:
        logger.warning('===== ACTIVE PAYMENTS (WAITING TO BE SENT) =====')
        logger.warning('%d payment files to process', len(paymentfiles))
        logger.warning('files in alphabetical order are:')
        for p in paymentfiles:
            logger.warning('  %s', p)

    # Report on failed payment files
    failedpayments = sorted(glob.glob(config.PAYOUTFAILDIR + '/*'))
    if len(failedpayments) == 0:
        logger.info('no failed payments')
    else:
        logger.warning('===== FAILED PAYMENTS (COULD NOT BE SENT) =====')
        logger.warning('%d failed payment files', len(failedpayments))
        logger.warning('files in alphabetical order are:')
        for f in failedpayments:
            logger.warning('  %s', f)

    # Report on database: what is the last timestamp
    logger.info('===== RECENCY OF ARK NODE DATABASE =====')
    max_timestamp = ark.Node.max_timestamp()
    logger.info('max blocks timestamp: %s', utils.arktimestamp(max_timestamp))


if __name__ == '__main__':
    # Set op logging
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

    # Run main, catch any exception and report.
    try:
        main()
    except:
        logger.warning('caught exception in payoutreporter')
        logger.fatal('stopping after exception')
