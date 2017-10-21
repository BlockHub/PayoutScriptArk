from arky import api, core
import acidfile
import datetime
import config
import urllib.request
import json
import utils
import pickle


def send(address, amount, test):
    if test:
            print('sent ', amount/utils.ARK, 'to ', address)
    else:
        tx = core.Transaction(amount=amount, recipientId=address)
        result = api.broadcast(tx, config.SECRET)
        print('transactionID = ', result["transactionIds"][0])


def send_transactions(payouts, frq_dict, test=None):
    api.use('ark')
    day_month = datetime.datetime.today().month
    day_week = datetime.datetime.today().weekday()
    totalfees = 0
    current_timestamp = utils.get_current_timestamp()

    if config.SHARE['COVER_TX_FEES']:
        fees = 0
    else:
        fees = config.SHARE['FEES']

    for address in payouts:
        if address in config.EXCEPTIONS:
            amount = ((payouts[address]['share'] * config.EXCEPTIONS[address]) - fees)
        else:
            for i in config.SHARE['TIMESTAMP_BRACKETS']:
                if payouts[address]['vote_timestamp'] < i:
                    amount = ((payouts[address]['share'] * config.SHARE['TIMESTAMP_BRACKETS'][i]) - fees)

        if address in frq_dict:
            frequency = frq_dict[address]
        else:
            frequency = 2

        if frequency == 1:
            if payouts[address]['last_payout'] < current_timestamp - (3600 * 20):
                if amount > config.SHARE['MIN_PAYOUT_BALANCE_DAILY']:
                    totalfees += config.SHARE['FEES']
                    send(address, amount, test=test)
        elif frequency == 2 and day_week == 4:
            if payouts[address]['last_payout'] < current_timestamp - (3600 * 24):
                if amount > config.SHARE['MIN_PAYOUT_BALANCE_WEEKLY']:
                    totalfees += config.SHARE['FEES']
                    send(address, amount, test=test)
        elif frequency == 3 and day_month == 28:
            if payouts[address]['last_payout'] < current_timestamp - (3600 * 24 * 24):
                if amount > config.SHARE['MIN_PAYOUT_BALANCE_MONTHLY']:
                    totalfees += config.SHARE['FEES']
                    send(address, amount, test=test)

    print(delegateshare/utils.ARK)
    print(totalfees/utils.ARK)
    print(len(payouts))
    delegateamount = (delegateshare - (totalfees))
    send(config.DELEGATE['REWARDWALLET'], delegateamount, test=test)


def get_frequency(use_site=None):
    frq_dict = {}
    if use_site:
        with urllib.request.urlopen("dutchdelegates.nl/api/user/") as url:
            data = json.loads(url.read().decode())

        for user in data['objects']:
            frq_dict.update({user['wallet']: user['payout_frequency']})
    else:
        data = config.FREQUENCY_DICT
        for user in data['objects']:
            frq_dict.update({user: data['objects'][user]})

    return frq_dict


if __name__ == '__main__':
    d = acidfile.ACIDDir(config.PAYOUTDIR)
    for f in d.glob():
        with acidfile.ACIDReadFile(f) as inf:
            data = pickle.load(inf)
            send_transaction(data, test=True)
    """
    save_file = 'payouts_{}'.format(datetime.date.today())

    with open(save_file, 'rb') as f:
        payouts_and_delegateshare = pickle.load(f)
        f.close()

    payouts, delegateshare = payouts_and_delegateshare
    frq_dict = get_frequency(config.CONNECTION['USE_API'])
    send_transactions(payouts, frq_dict, test=True)
    """
