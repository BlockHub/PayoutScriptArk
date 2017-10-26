import utils

# How to connect to the Ark node Postgresql database.
CONNECTION = {
    'HOST'    : "localhost",
    'DATABASE': "ark_mainnet",
    'USER'    : "payoutscript",
    'USE_API' :  None,
    'PASSWORD': 'dwleml123'
    }

CALCULATIONS = {
    # amount of blocks to calculate backwards to. Should be determined by
    # the voter waiting for a payout the longest.
    'blocks': 6874
}

# Who are we: the delegate's info.
DELEGATE = {
    'PUBKEY'      : "0218b77efb312810c9a549e2cc658330fcc07f554d465673e08fa304fa59e67a0a",
    'ADDRESS'     : "AZse3vk8s3QEX1bqijFb21aSBeoF6vqLYE",
    'PASSPHRASE'  : None,
    'REWARDWALLET': 'ASYtfgrzdG4A9p5TFDhg22cE7FnV71AHxM'
    }

# How are fees calculated.
SHARE = {
    'FEES'     : 0.1 * 100000000,
    'FLAT_TAX' : None,
    'BLACKLIST': None,

    # The default share, when TIMESTAMP_BRACKETS (see below) do not apply.
    'DEFAULT_SHARE': 0.95,

    # TIMESTAMP_BRACKETS do not redistribute the amounts to lower brackets,
    # proceeds go to delegate
    # If TIMESTAMP_BRACKETS and BALANCE_BRACKETS are both not None, they are
    # both applied: I.E. above
    # 200k Ark = 80% share, and if voted after 8th of september = 90% share,
    # the total share for this voter
    # is 80% * 90% = 0.64%.
    'TIMESTAMP_BRACKETS':
    {
        float('inf'): 0.95,
        16247647    : 0.96
    },

    # BALANCE_BRACKETS do not redistribute the amounts to lower brackets,
    # proceeds go to delegate
    'BALANCE_BRACKETS': None,

    # any balance above max balance or below min balance is not taken in the
    # calculation (the ark is divided amongst voters and delegate)
    # so if MAX_BALANCE == 200k and a voter has
    # 300k, it is counted as 200K.
    # If a voter has 1 Ark, and MIN_BALANCE == 2 Ark, it is counted as 0 Ark
    'MAX_BALANCE'                  : None,
    'MIN_BALANCE'                  : None,
    'MIN_PAYOUT_BALANCE_DAILY'     : 3 * utils.ARK,
    'MIN_PAYOUT_BALANCE_WEEKLY'    : 0.1 * utils.ARK,
    'MIN_PAYOUT_BALANCE_MONTHLY'   : 0.1 * utils.ARK,
    'COVER_TX_FEES'                : True,
    'COVER_VOTING_FEES'            : False,
    'MAX_BALANCE_COVER_TX_FEES'    : False,
    'MIN_BALANCE_COVER_VOTING_FEES': False,

    # At the end of the personal message a tag could be included for
    # administrative purposes
    # Example: 'Thanks for voting! ::VOTINGFEE::
    'PERSONAL_MESSAGE': None,

}

# Custom payout schemes on a per-voter basis. E.g., you can give a higher
# share than the default to early adopters.
EXCEPTIONS = {'AQ9gNYefdLE83GpfTzc1pPyCZgX6KvV9rm': 0.96,
              'APGjeMNZY99WuzZi18NUb8RowEscLV7F7M': 0.96,
              }

# Blacklisted voters: whom do we never wish to pay out.
BLACKLIST = ['AXzEMF7TC1aH3ax1Luxk6XdyKXDRxnBj4f', ]

# Secret key for broadcasting to the Ark network.
SECRET = 'string'

# 1 = daily
# 2 = weekly, saturday
# 3 = monthly, on the 28th

FREQUENCY_DICT = {
    'objects':{
        'address': 1,               
    }
}

# The payout files will appear in this directory for further processing.
# The payout script will create the directory if it doesn't exist yet.
PAYOUTDIR     = '/home/ark/payouts'
# Failed payouts will be moved here for closer inspection:
PAYOUTFAILDIR = '/home/ark/failedpayouts'

# Where to log stuff. This will be rotated so that the disk doesn't fill
# up like crazy.
LOGGING = {
    # log to this file and create -1, -2 etc. for historical versions
    'logfile'  : '/tmp/ark.log',
    # debugging: on or off
    'verbosity': True,
    # max size of the logfile before it gets rotated to <file>-1
    'maxsize'  : 1024 * 1024
}

# This enables the testmode in the payout sender. No payouts are sent,
# only log statements are generated.
PAYOUTSENDER_TEST = True
