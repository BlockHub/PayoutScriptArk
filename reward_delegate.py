import arkdbtools.dbtools
import arkdbtools.config as constants
import config
from arky import api, core


def calculate_delegate_share():
    arkdbtools.dbtools.set_connection(
            host=config.CONNECTION['HOST'],
            database=config.CONNECTION['DATABASE'],
            user=config.CONNECTION['USER'],
            password=config.CONNECTION['PASSWORD'])

    payouts = arkdbtools.dbtools.Address.transactions(config.DELEGATE['ADDRESS'])

    last_reward_payout = arkdbtools.dbtools.DbCursor().execute_and_fetchone("""
        SELECT transactions."timestamp"
        FROM transactions
        WHERE transactions."recipientId" = '{rewardwallet}'
        AND transactions."senderId" = '{delegateaddress}'
        ORDER BY transactions."timestamp" DESC 
        LIMIT 1
    """.format(
        rewardwallet=config.DELEGATE['REWARDWALLET'],
        delegateaddress=config.DELEGATE['ADDRESS']
    ))[0]
    delegate_share = 0
    if config.SENDER_SETTINGS['COVER_TX_FEES']:
        txfee = constants.TX_FEE
    else:
        txfee = 0

    for i in payouts:
        if i.recipientId == config.DELEGATE['REWARDWALLET']:
            del i
        else:
            if i.timestamp > last_reward_payout:
                total_send_amount = (i.amount + txfee) / config.SENDER_SETTINGS['DEFAULT_SHARE']
                delegate_share += (total_send_amount) - (total_send_amount * config.SENDER_SETTINGS['DEFAULT_SHARE'] + txfee)

    return delegate_share


def send_delegate_share(amount):
    api.use(network='ark')
    tx = core.Transaction(
        amount=amount,
        recipientId=config.DELEGATE['REWARDWALLET'])

    if config.DELEGATE['SECOND_SECRET']:
        tx.sign(secret=config.DELEGATE['SECRET'],
                secondSecret=config.DELEGATE['SECOND_SECRET'])
    else:
        tx.sign(secret=config.DELEGATE['SECRET'])

    tx.serialize()

    res = api.sendTx(
        tx=tx,
        url_base=config.IP,
        secret=config.DELEGATE['SECRET'],
        secondSecret=config.DELEGATE['SECOND_SECRET'])
    return res


if __name__ == '__main__':
    delegate_address = 'ALUeCYpPvPUMt9FUEWWf2xAoaX3WXo9hou'
    reward = calculate_delegate_share()
    res = send_delegate_share(reward)
