from arky import api
from collections import namedtuple
from tabulate import tabulate

import acidfile
import config
import copy
import datetime
import os
import parky
import pickle
import rotlog as rl
import sys
import time
import traceback
import utils

def get_transactionlist(cursor):
    command = """
        SELECT transactions."id", transactions."amount",
               transactions."timestamp", transactions."recipientId",
               transactions."senderId", transactions."rawasset",
               transactions."type", transactions."fee"
        FROM transactions
        WHERE transactions."timestamp" <= {0}
        AND transactions."senderId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{1}')
        OR transactions."recipientId" IN
          (SELECT transactions."recipientId"
           FROM transactions, votes
           WHERE transactions."id" = votes."transactionId"
           AND votes."votes" = '+{1}')
        ORDER BY transactions."timestamp" ASC;""".format(
            utils.get_max_timestamp(cursor=cursor),
            config.DELEGATE['PUBKEY'])

    cursor.execute(command)
    return cursor.fetchall()


def name_transactionslist(transactions):
    Transaction = namedtuple(
        'transaction',
        'id amount timestamp recipientId senderId rawasset type fee')
    named_transactions = []
    for i in transactions:
        tx_id = Transaction(id=i[0],
                            amount=i[1],
                            timestamp=i[2],
                            recipientId=i[3],
                            senderId=i[4],
                            rawasset=i[5],
                            type=i[6],
                            fee=i[7],
                            )

        named_transactions.append(tx_id)

    if len(transactions) != len(named_transactions):
        raise utils.NameError('Length of named transactions is not equal '
                              'to query from DB')
    return named_transactions


def get_all_voters(cursor):
    command = """SELECT transactions."recipientId", transactions."timestamp"
                 FROM transactions, votes
                 WHERE transactions."timestamp" <= {0}
                 AND transactions."id" = votes."transactionId"
                 AND votes."votes" = '+{1}';""".format(
                     utils.get_max_timestamp(cursor=cursor),
                     config.DELEGATE['PUBKEY'])

    cursor.execute(command)
    return cursor.fetchall()


def create_voterdict(res):
    voter_dict = {}
    for i in res:
        voter_dict.update({i[0]:{'balance': 0,
                                 'status': False,
                                 'last_payout': i[1],
                                 'share': 0,
                                 'vote_timestamp': i[1]}})

    # len(res) != len(voterdict) because some people have unvoted and revoted
    # (and keys need to be hashable)
    return voter_dict


def get_blocks(cursor):
    command = """SELECT blocks."timestamp", blocks."height", blocks."id"
                 FROM blocks
                 WHERE blocks."timestamp" <= {0}
                 AND blocks."generatorPublicKey" = '\\x{1}'
                 ORDER BY blocks."timestamp" ASC""".format(
                     utils.get_max_timestamp(cursor=cursor),
                     config.DELEGATE['PUBKEY'])

    cursor.execute(command)
    return cursor.fetchall()


def name_blocks(get_blocks):
    Block = namedtuple('block',
                       'timestamp height id')
    block_list = []
    for block in get_blocks:
        block_value = Block(timestamp=block[0],
                            height=block[1],
                            id=block[2],)
        block_list.append(block_value)

    if len(get_blocks) == len(block_list):
        return block_list
    else:
        raise utils.NameError('Length of named blocks is not equal to query '
                              'from DB')


def parse(tx, dict):
    if tx.recipientId in dict and tx.type == 0:
        dict[tx.recipientId]['balance'] += tx.amount
    if tx.senderId in dict and tx.type == 0:
        dict[tx.senderId]['balance'] -= (tx.amount + tx.fee)
    if tx.senderId in dict and tx.type == 2 or tx.type == 3:
        dict[tx.senderId]['balance'] -= tx.fee

    minvote  = '{{"votes":["-{0}"]}}'.format(config.DELEGATE['PUBKEY'])
    plusvote = '{{"votes":["+{0}"]}}'.format(config.DELEGATE['PUBKEY'])
    if tx.type == 3 and minvote in tx.rawasset:
        dict[tx.recipientId]['status'] = False
    if tx.type == 3 and plusvote in tx.rawasset:
        dict[tx.recipientId]['status'] = True
        dict[tx.recipientId]['vote_timestamp'] = tx.timestamp

    if tx.senderId == config.DELEGATE['ADDRESS']:
        dict[tx.recipientId]['last_payout'] = tx.timestamp
    return dict


def parse_tx(all_tx, voter_dict, named_blocks):
    balance_dict = {}
    block_nr = 0
    for tx in all_tx:
        if tx.timestamp >= named_blocks[block_nr].timestamp:
            res = copy.deepcopy(voter_dict)
            balance_dict.update({named_blocks[block_nr].timestamp: res})
            block_nr += 1
        voter_dict = parse(tx, voter_dict)
    return balance_dict


def cal_share(balance_dict):
    # calculating total pool_balance and relative share per voter
    # this part could also be performed in parse_tx
    for voter_dict in balance_dict:
        pool_balance = 0
        for i in balance_dict[voter_dict]:
            if (balance_dict[voter_dict][i]['status'] and
                i not in config.BLACKLIST):
                pool_balance += balance_dict[voter_dict][i]['balance']
        for i in balance_dict[voter_dict]:
            if (balance_dict[voter_dict][i]['status'] and
                i not in config.BLACKLIST):
                balance_dict[voter_dict][i]['share'] = (
                    balance_dict[voter_dict][i]['balance'] / pool_balance)
    return balance_dict


def stretch(dict, blocks):
    # duplicating block_dicts where there were no voter transactions during
    # 6.8 minute interval
    # this makes len(payout_dict) = len(blocks)
    temp_dic = {}
    last_block = min(dict.keys())

    for block in blocks:
        if block.timestamp not in dict.keys():
            temp_dic.update({block.timestamp: dict[last_block]})
        elif block.timestamp in dict.keys():
            last_block = block.timestamp

    dict.update(temp_dic)

    return dict


def gen_payouts(final_balance_dict, blocks):

    # returns a dict with address as key, and total amount of ark to be
    # transacted for X blocks
    delegateshare = 0
    blocks.reverse()
    payout_dict = {}
    last_block = max(final_balance_dict.keys())
    for block in final_balance_dict:
        for address in final_balance_dict[block]:
            if config.SHARE['TIMESTAMP_BRACKETS']:
                for i in config.SHARE['TIMESTAMP_BRACKETS']:
                    if (final_balance_dict[block][address]['vote_timestamp']
                        <= i):
                        share = config.SHARE['TIMESTAMP_BRACKETS'][i]
                    else:
                        share = config.SHARE['DEFAULT_SHARE']
                        if address in config.EXCEPTIONS:
                            share = config.EXCEPTIONS[address]
                    tax = 1 - share

            if final_balance_dict[last_block][address]['last_payout'] < block:
                if address not in payout_dict:
                    payout_dict.update({address: {
                        'share':
                        (final_balance_dict[block][address]['share'] * 2 *
                         utils.ARK * share),
                        'last_payout':
                        final_balance_dict[last_block][address]['last_payout'],
                        'vote_timestamp':
                        final_balance_dict[last_block][address]['vote_timestamp'],
                        'status':
                        final_balance_dict[last_block][address]['status']}}
                                                      )
                    delegateshare += (
                        final_balance_dict[block][address]['share'] * 2 *
                        utils.ARK * tax)
                else:
                    payout_dict[address]['share'] += (
                        final_balance_dict[block][address]['share'] * 2 *
                        utils.ARK * share)
                    delegateshare += (
                        final_balance_dict[block][address]['share'] * 2 *
                        utils.ARK * tax)

    return payout_dict, delegateshare


def test_print(payouts, delegateshare, set_api=None):
    if set_api:
        api.use('ark')

    table = []
    ROI = 0
    balance = 0
    for i in payouts:
        info = []
        share = (payouts[i]['share'])
        if set_api:
            for x in range(5):
                try:
                    req = api.Account.getBalance(i)
                    balance = float(req['balance'])
                    if balance != 0:
                        ROI = (share * 52) / balance * 100
                    break
                except Exception:
                    time.sleep(1)
                    pass
        status = payouts[i]['status']
        last_payout = payouts[i]['last_payout']
        info.append([i, share/utils.ARK, ROI ,
                     balance/utils.ARK, last_payout, status])
        table.append(info)

    total = 0
    for i in payouts:
        total += payouts[i]['share']

    rl.debug(tabulate(table, ['ADDRESS', 'SHARE', 'ROI', 'BALANCE', 'STATUS']))
    rl.debug('total to be paid: %s, delegateshare before txfees: %s',
             str(total), str(delegateshare))


def main():
    ts = utils.get_max_timestamp()
    rl.info('going up to arktimestamp %s', utils.arctimestamp(ts))

    # Create the payout dir if it doesn't exist yet.
    os.makedirs(config.PAYOUTDIR, exist_ok=True)

    # initialize DB cursor
    cursor = parky.DbCursor()

    # execute all sql queries first, since the DB is updated every 8 seconds,
    # the odds of the data having changed is lower.
    rl.debug('fetching blocks')
    unnamed_blocks = get_blocks(cursor)

    rl.debug('fetching transactions')
    unnamed_transactions = get_transactionlist(cursor)

    rl.debug('fetching voters')
    voter_list = get_all_voters(cursor)

    # naming the query objects (mainly for making the code more readable, does
    # decrease performance by an itsy bitsy
    rl.debug('naming blocks')
    named_blocks = name_blocks(unnamed_blocks)

    rl.debug('naming transactions')
    named_transactions = name_transactionslist(unnamed_transactions)

    rl.debug('naming voters')
    voter_dict = create_voterdict(voter_list)

    number_of_blocks = config.CALCULATIONS['blocks']
    rl.debug('considering %d blocks', number_of_blocks)

    # calculate balances over time for every voter
    rl.debug('getting balance over time for all voters')
    balance_dict = parse_tx(named_transactions, voter_dict, named_blocks)

    # calculate the total pool balance and share per voter
    rl.debug('determining pool balance and share per voter')
    updated_balance_dict = cal_share(balance_dict)

    # stretch the balances over time to make sure it is the same length as
    # the total number of blocks. (sometimes there is no transaction at all for
    # multiples of 6.8 minutes, so then the last calculated block balance is
    # used for the empty blocks.
    rl.debug('stretching balance info to fill empty blocks')
    balance_history = stretch(updated_balance_dict, named_blocks)

    rl.debug('generating payouts and delegates share')
    payouts_and_delegateshare = gen_payouts(balance_history, named_blocks)
    test_print(payouts_and_delegateshare[0], payouts_and_delegateshare[1],
               set_api=False)
    # Write all payout data.
    stamp = utils.timestamp(forfilename=True)
    rl.info('writing %s/%s*', config.PAYOUTDIR, stamp)
    nfiles = 0
    for address in payouts_and_delegateshare[0].keys():
        nfiles += 1
        savefile = '%s/%s-%s' % (config.PAYOUTDIR, stamp, address)
        data = [address, payouts_and_delegateshare[0][address]]
        rl.debug('data for voter payment file %s: %s', savefile, str(data))
        with acidfile.ACIDWriteFile(savefile) as outfile:
            pickle.dump(data, outfile)

    delegate_file = '%s/%s-%s' % (config.PAYOUTDIR, stamp,
                                  config.DELEGATE['REWARDWALLET'])
    data = [config.DELEGATE['REWARDWALLET'], payouts_and_delegateshare[1]]
    rl.debug('data for delegate payment file %s: %s', delegate_file, str(data))
    nfiles += 1
    with acidfile.ACIDWriteFile(delegate_file) as outfile:
        pickle.dump(data, outfile)

    rl.info('%d files written (including payout to reward wallet)', nfiles)
    rl.info('finished')

if __name__ == '__main__':
    # Initialize logging
    utils.setuplogging('payoutcalculator')

    # Protect the entire run in a try block so we get postmortem info if
    # applicable.
    try:
        main()
    except Exception as e:
        tp, vl, tb = sys.exc_info()
        for line in traceback.format_exception(tp, vl, tb):
            line = line.replace('\n', ' ')
            rl.warn('caught exception in main: %s', line)
        rl.fatal('stopping after exception')
