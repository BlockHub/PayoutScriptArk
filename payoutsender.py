from arky import api, core
import acidfile
import datetime
import config
import urllib.request
import json
import utils
import pickle
import os
import rotlog as rl
import sys

class TransactionError(Exception):
    pass


def send(address, amount):
    if config.PAYOUTSENDER_TEST:
        rl.info('would send %f to %s', amount/utils.ARK, address)
        return True

    tx = core.Transaction(amount=amount, recipientId=address)
    result = api.broadcast(tx, config.SECRET)
    if result['success']:
        return True

    rl.warn('payout to {0} for amount {1} failed. Response: {2}'.
            format(address, amount, result))
    return False


def send_transaction(data, frq_dict, max_timestamp):
    # data[0] is always the address.
    # data[1] can differ: for voters it is a map having keys
    #         last_payout, status, share and vote_timestamp.
    #         For transactions towards the reward wallet it is just one
    #         float, the reward.

    day_month = datetime.datetime.today().month
    day_week = datetime.datetime.today().weekday()
    totalfees = 0
    address = data[0]
    amount = 0
    if config.SHARE['COVER_TX_FEES']:
        fees = 0
    else:
        fees = config.SHARE['FEES']
    if address in config.EXCEPTIONS:
        amount = ((data[1]['share'] * config.EXCEPTIONS[address]) - fees)
    else:
        if config.SHARE['TIMESTAMP_BRACKETS']:
            for i in config.SHARE['TIMESTAMP_BRACKETS']:
                if data[1]['vote_timestamp'] < i:
                    amount = ((data[1]['share'] *
                               config.SHARE['TIMESTAMP_BRACKETS'][i])
                              - fees)
        else:
            amount = ((data[1]['share'] *
            config.SHARE['DEFAULT_SHARE'])
            - fees)

    delegate_share = data[1]['share'] - amount

    if address in frq_dict:
        frequency = frq_dict[1]
    else:
        frequency = 2

    if frequency == 1:
        if data[1]['last_payout'] < max_timestamp - (3600 * 20):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_DAILY']:
                totalfees += config.SHARE['FEES']
                result = send(address, amount)
                return result, delegate_share

    elif frequency == 2 and day_week == 4:
        if data[1]['last_payout'] < max_timestamp - (3600 * 24):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_WEEKLY']:
                totalfees += config.SHARE['FEES']
                result = send(address, amount)
                return result, delegate_share

    elif frequency == 3 and day_month == 28:
        if data[1]['last_payout'] < max_timestamp - (3600 * 24 * 24):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_MONTHLY']:
                totalfees += config.SHARE['FEES']
                result = send(address, amount)
                return result, delegate_share
    return 0


def get_frequency(use_site=None):
    frq_dict = {}
    if use_site:
        with urllib.request.urlopen("https://www.dutchdelegate.nl/api/user/") as url:
            data = json.loads(url.read().decode())
        for user in data['objects']:
            frq_dict.update({user['main_ark_wallet']: user['payout_frequency']})
    else:
        data = config.FREQUENCY_DICT
        for user in data['objects']:
            frq_dict.update({user: data['objects'][user]})
    return frq_dict


def main():
    # Create a dir for the failed payments if it doesn't exist yet.
    os.makedirs(config.PAYOUTFAILDIR, exist_ok=True)
    delegate_share = 0
    api.use('ark')
    max_timestamp = utils.get_max_timestamp()
    frq_dict = get_frequency(None)

    d          = acidfile.ACIDDir(config.PAYOUTDIR)
    files      = d.glob()
    filenr     = 0
    nsucceeded = 0
    nfailed    = 0
    if not len(files):
        rl.fatal('no files to process in %s', config.PAYOUTDIR)

    for f in files:
        filenr += 1
        rl.debug('picking up payment file %s (%d of %d)',
                 f, filenr, len(files))
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
                res = send_transaction(data, frq_dict, max_timestamp)
                if res[0]:
                    delegate_share += res[1]
                    nsucceeded += 1
            except:
                rl.warn('exception while processing payment file %s with '
                        'data %s', f, data)
                rl.warn(rl.formatexception())
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
                rl.warn('problem processing payment file, moved to %s',
                        newfile)
                os.rename(f, newfile)

    # All done, let's see how we did
    rl.info('of %d files, %d failed and %d succeeded',
            filenr, nfailed, nsucceeded)

    send(config.DELEGATE['ADDRESS'], delegate_share)

if __name__ == '__main__':
    # Initialize logging.
    utils.setuplogging('payoutsender')

    # Protect the entire run in a try block so we get postmortem info if
    # applicable.
    try:
        main()
    except:
        rl.warn('caught exception in payoutsender')
        rl.warn(rl.formatexception())
        rl.fatal('stopping after exception')
