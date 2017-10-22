import config
import glob
import rotlog as rl
import sys
import traceback
import utils

def main():
    # Report on active payment files
    rl.info('===== ACTIVE PAYMENTS (TO BE SENT) =====')
    paymentfiles = sorted(glob.glob(config.PAYOUTDIR + '/*'))
    if len(paymentfiles) == 0:
        rl.info('no payment files to process')
    else:
        rl.info('%d payment files to process', len(paymentfiles))
        rl.info('files in alphabetical order are:')
        for p in paymentfiles:
            rl.info('  %s', p)

    # Report on failed payment files
    rl.info('===== FAILED PAYMENTS (COULD NOT BE SENT) =====')
    failedpayments = sorted(glob.glob(config.PAYOUTFAILDIR + '/*'))
    if len(failedpayments) == 0:
        rl.info('no failed payments')
    else:
        rl.info('%d failed payment files', len(failedpayments))
        rl.info('files in alphabetical order are:')
        for f in failedpayments:
            rl.info('  %s', f)

    # Report on database: what is the last timestamp
    rl.info('===== RECENCY OF ARK NODE DATABASE =====')
    max_timestamp = utils.get_max_timestamp()
    rl.info('max blocks timestamp: %s', utils.arctimestamp(max_timestamp))


if __name__ == '__main__':
    # Set op logging
    utils.setuplogging('payoutreporter')

    # Run main, catch any exception and report.
    try:
        main()
    except Exception as e:
        tp, vl, tb = sys.exc_info()
        for line in traceback.format_exception(tp, vl, tb):
            line = line.replace('\n', ' ')
            rl.warn('caught exception in main: %s', line)
            rl.fatal('stopping after exception')
