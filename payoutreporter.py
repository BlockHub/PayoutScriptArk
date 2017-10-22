import config
import glob
import rotlog as rl
import sys
import utils

def main():
    # Report on active payment files
    paymentfiles = sorted(glob.glob(config.PAYOUTDIR + '/*'))
    if len(paymentfiles) == 0:
        rl.info('no payment files to process')
    else:
        rl.warn('===== ACTIVE PAYMENTS (WAITING TO BE SENT) =====')
        rl.warn('%d payment files to process', len(paymentfiles))
        rl.warn('files in alphabetical order are:')
        for p in paymentfiles:
            rl.warn('  %s', p)

    # Report on failed payment files
    failedpayments = sorted(glob.glob(config.PAYOUTFAILDIR + '/*'))
    if len(failedpayments) == 0:
        rl.info('no failed payments')
    else:
        rl.warn('===== FAILED PAYMENTS (COULD NOT BE SENT) =====')
        rl.warn('%d failed payment files', len(failedpayments))
        rl.warn('files in alphabetical order are:')
        for f in failedpayments:
            rl.warn('  %s', f)

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
    except:
        rl.warn('caught exception in payoutreporter')
        rl.warn(rl.formatexception())
        rl.fatal('stopping after exception')
