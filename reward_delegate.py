import arkdbtools.dbtools
import arkdbtools.config as constants
import config
from arky import api, core
import logging.handlers


def calculate_delegate_share():
    arkdbtools.dbtools.set_connection(
            host=config.CONNECTION['HOST'],
            database=config.CONNECTION['DATABASE'],
            user=config.CONNECTION['USER'],
            password=config.CONNECTION['PASSWORD'])

    payouts = arkdbtools.dbtools.Address.transactions(config.DELEGATE['ADDRESS'])
    blocks = arkdbtools.dbtools.Delegate.blocks(config.DELEGATE['PUBKEY'])

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
                delegate_share += total_send_amount - (total_send_amount * config.SENDER_SETTINGS['DEFAULT_SHARE'] + txfee)

    for b in blocks:
        if b.timestamp > last_reward_payout:
            delegate_share += b.totalFee

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
    logger = logging.getLogger(__name__)
    handler = logging.handlers.RotatingFileHandler(config.LOGGING['LOGDIR'],
                                                   encoding='utf-8',
                                                   maxBytes=10 * 1024 * 1024,
                                                   backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    reward = calculate_delegate_share()
    if config.REWARD_DELEGATE_TEST:
        logger.info('DELEGATE REWARD: {}'.format(reward))
    else:
        res = send_delegate_share(reward)
