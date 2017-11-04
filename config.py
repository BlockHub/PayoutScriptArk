import logging
import arkdbtools.config as info


CONNECTION = {
    'HOST': None,
    'DATABASE': None,
    'USER': None,
    'PASSWORD': None,
}





# Who are we: the delegate's info.
DELEGATE = {
    'PUBKEY'      : None,
    'ADDRESS'     : None,
    'PASSPHRASE'  : None,
    'REWARDWALLET': None,
    }

# How are fees calculated.
SENDER_SETTINGS = {
    'FEES'     : info.TX_FEE,
    'FLAT_TAX' : None,
    'BLACKLIST': None,

    # The default share, when TIMESTAMP_BRACKETS (see below) do not apply.
    'DEFAULT_SHARE': 0.96,

    # TIMESTAMP_BRACKETS do not redistribute the amounts to lower brackets,
    # proceeds go to delegate
    # If TIMESTAMP_BRACKETS and BALANCE_BRACKETS are both not None, they are
    # both applied: I.E. above
    # 200k Ark = 80% share, and if voted after 8th of september = 90% share,
    # the total share for this voter
    # is 80% * 90% = 0.64%.
    'TIMESTAMP_BRACKETS': None,

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
    'MIN_PAYOUT_BALANCE_DAILY'     : 2,
    'MIN_PAYOUT_BALANCE_WEEKLY'    : 0.1,
    'MIN_PAYOUT_BALANCE_MONTHLY'   : 0.001,
    'COVER_TX_FEES'                : False,
    'MAX_BALANCE_COVER_TX_FEES'    : False,
    'MIN_BALANCE_COVER_VOTING_FEES': False,

    # At the end of the personal message a tag could be included for
    # administrative purposes
    # Example: 'Thanks for voting! ::VOTINGFEE::
    'PERSONAL_MESSAGE': None,
    'DAY_WEEKLY_PAYOUT': 5,
    'DAY_MONTHLY_PAYOUT': 15,
    'WAIT_TIME_DAILY': 20*info.HOUR_SEC

}

# Custom payout schemes on a per-voter basis. E.g., you can give a higher
# share than the default to early adopters.
SHARE_EXCEPTIONS = None

# Blacklisted voters: whom do we never wish to pay out.
BLACKLIST = None

# Secret key for broadcasting to the Ark network.
SECRET = 'string'

# 1 = daily
# 2 = weekly, saturday
# 3 = monthly, on the 28th

FREQUENCY_DICT = {
        'address': 1,               
    }

HARD_EXCEPTIONS = None

# The payout files will appear in this directory for further processing.
# The payout script will create the directory if it doesn't exist yet.
PAYOUTDIR     = '/home/ark/payouts'
# Failed payouts will be moved here for closer inspection:
PAYOUTFAILDIR = '/home/ark/failedpayouts'

# Where to log stuff. This will be rotated so that the disk doesn't fill
# up like crazy.
LOGGING = {
    # log to this file and create -1, -2 etc. for historical versions
    'LOGDIR'  : '/tmp/payoutscriptark.log',
    'LOGGING_LEVEL': logging.INFO
}

# This enables the testmode in the payout sender. No payouts are sent,
# only log statements are generated.
PAYOUTCALCULATOR_TEST = True
PAYOUTSENDER_TEST = True
