import logging.handlers
import acidfile
import datetime
import config
import urllib.request
import json
import pickle
import os
import sys
import arkdbtools.config as info
from arky import api, core
import arkdbtools.dbtools as ark

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


class TransactionError(Exception):
    pass


def main():
    # Create a dir for the failed payments if it doesn't exist yet.
    os.makedirs(config.PAYOUTFAILDIR, exist_ok=True)
    delegate_share = 0
    total_to_be_sent = 0
    fees = 0
    api.use('ark')
    max_timestamp = ark.Node.max_timestamp()


    d          = acidfile.ACIDDir(config.PAYOUTDIR)
    files      = d.glob()
    filenr     = 0
    nsucceeded = 0
    nfailed    = 0

    if not len(files):
        logger.fatal('no files to process in %s', config.PAYOUTDIR)

    for f in files:
        filenr += 1
        logger.debug('picking up payment file %s (%d of %d)',
                 f, filenr, len(files))
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
        with acidfile.ACIDReadFile(f) as inf:
            # Assume sending failure. We might be surprised later on if all
            # this actually works :-)
            result = False

            # Handle unpickling and data interpretation in a try block.
            # It is on a per-file basis and we don't want to crash the whole
            # run, we want to report on the failure and continue onto the next
            # payment file.
            try:
                data = pickle.load(inf)
                result, delegate_reward, amount = ark.Core.payoutsender(data, max_timestamp)

                logger.debug('result of send: {}'.format(result))
                if result:
                    delegate_share += delegate_share
                    total_to_be_sent += amount
                    fees += config.SENDER_SETTINGS['FEES']
                    nsucceeded += 1
            except Exception:
                logger.warning('exception while processing payment file %s with '
                        'data %s', f, data)
                nfailed += 1

            if config.PAYOUTSENDER_TEST:
                # When in testmode, never mind about the result. Continue
                # to the next file, leave files that caused errors or files
                # that parsed correctly where they were.
                continue

            # Interpret the sending result only if we are not in testmode.
            if result:
                os.remove(f)
            else:
                newfile = config.PAYOUTFAILDIR + '/' + os.path.basename(f)
                logger.warning('problem processing payment file, moved to %s',
                        newfile)
                os.rename(f, newfile)

    # All done, let's see how we did
    logger.info('of %d files, %d failed and %d succeeded',
            filenr, nfailed, nsucceeded)
    logger.info('Delegatereward: {}   Total to be sent to voters: {}  Total fees: {}'.format(delegate_share/info.ARK,
                                                                                         total_to_be_sent/info.ARK,
                                                                                         fees/info.ARK))
    ark.Core.send(config.DELEGATE['REWARDWALLET'], delegate_share)


if __name__ == '__main__':
    # Initialize logging.

    # Protect the entire run in a try block so we get postmortem info if
    # applicable.
    try:
        main()
    except Exception:
        logger.warning('caught exception in payoutsender')
        logger.fatal('stopping after exception')
