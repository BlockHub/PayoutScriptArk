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


def send_transaction(data, frq_dict, current_timestamp, test=None):
    day_month = datetime.datetime.today().month
    day_week = datetime.datetime.today().weekday()
    totalfees = 0

    if config.SHARE['COVER_TX_FEES']:
        fees = 0
    else:
        fees = config.SHARE['FEES']

    address = data[0]

    if address in config.EXCEPTIONS:
        amount = ((data[1]['share'] * config.EXCEPTIONS[address]) - fees)
    else:
        for i in config.SHARE['TIMESTAMP_BRACKETS']:
            if data[address]['vote_timestamp'] < i:
                amount = ((data[1]['share'] * config.SHARE['TIMESTAMP_BRACKETS'][i]) - fees)
            else:
                amount = ((data[1]['share'] * 0.95) - fees)

    if address in frq_dict:
        frequency = frq_dict[1]
    else:
        frequency = 2

    if frequency == 1:
        if data[1]['last_payout'] < current_timestamp - (3600 * 20):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_DAILY']:
                totalfees += config.SHARE['FEES']
                send(address, amount, test=test)
    elif frequency == 2 and day_week == 4:
        if data[1]['last_payout'] < current_timestamp - (3600 * 24):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_WEEKLY']:
                totalfees += config.SHARE['FEES']
                send(address, amount, test=test)
    elif frequency == 3 and day_month == 28:
        if data[1]['last_payout'] < current_timestamp - (3600 * 24 * 24):
            if amount > config.SHARE['MIN_PAYOUT_BALANCE_MONTHLY']:
                totalfees += config.SHARE['FEES']
                send(address, amount, test=test)


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
    api.use('ark')
    current_timestamp = utils.get_current_timestamp()
    frq_dict = get_frequency(None)

    d = acidfile.ACIDDir(config.PAYOUTDIR)
    for f in d.glob():
        with acidfile.ACIDReadFile(f) as inf:
            data = pickle.load(inf)
            send_transaction(data, frq_dict, current_timestamp, test=True)
