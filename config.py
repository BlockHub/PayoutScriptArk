import utils


CONNECTION = {
    'HOST': "localhost",
    'DATABASE': "ark_mainnet",
    'USER': "ark",
    'USE_API': None
    }

CALCULATIONS = {
    # amount of blocks to calculate backwards to. Should be determined by the voter
    # waiting for a payout the longest.
    'blocks': 5000
}
DELEGATE = {
    'PUBKEY': "0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a",
    'ADDRESS': "AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE",
    'PASSPHRASE': None,
    'REWARDWALLET': 'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY'
    }

SHARE = {
    'FEES': 0.1 * 100000000,
    'FLAT_TAX': None,
    'BLACKLIST': None,

    # TIMESTAMP_BRACKETS do not redistribute the amounts to lower brackets, proceeds go to delegate
    # If TIMESTAMP_BRACKETS and BALANCE_BRACKETS are both not None, they are both applied: I.E. above
    # 200k Ark = 80% share, and if voted after 8th of september = 90% share, the total share for this voter
    # is 80% * 90% = 0.64%.
    'TIMESTAMP_BRACKETS':
        {
        float('inf'): 0.95,
        16247647: 0.96
        },

    # BALANCE_BRACKETS do not redistribute the amounts to lower brackets, proceeds go to delegate
    'BALANCE_BRACKETS': None,

    # any balance above max balance or below min balance is not taken in the calculation
    # (the ark is divided amongst voters and delegate) so if MAX_BALANCE == 200k and a voter has
    # 300k, it is counted as 200K. If a voter has 1 Ark, and MIN_BALANCE == 2 Ark, it is counted as 0 Ark
    'MAX_BALANCE': None,
    'MIN_BALANCE': None,
    'MIN_PAYOUT_BALANCE_DAILY': 3 * utils.ARK,
    'MIN_PAYOUT_BALANCE_WEEKLY': 0.2 * utils.ARK,
    'MIN_PAYOUT_BALANCE_MONTHLY': 0.1 * utils.ARK,
    'COVER_TX_FEES': True,
    'COVER_VOTING_FEES': False,
    'MAX_BALANCE_COVER_TX_FEES': False,
    'MIN_BALANCE_COVER_VOTING_FEES': False,

    # At the end of the personal message a tag could be included for administrative purposes
    # Example: 'Thanks for voting! ::VOTINGFEE::
    'PERSONAL_MESSAGE': None,

}

EXCEPTIONS = {'AQ9gNYefdLE83GpfTzc1pPyCZgX6KvV9rm': 0.96,
              'APGjeMNZY99WuzZi18NUb8RowEscLV7F7M': 0.96,
              }

BLACKLIST = []

SECRET = 'string'

# 1 = daily
# 2 = weekly, saturday
# 3 = monthly, on the 28th

FREQUENCY_DICT = {
    'objects':{'address': 1,

                }
}