import logging
import arkdbtools.config as info

# all values used throughout the script are in ark-satoshis, except for the logging of the payouts,
# to make it more readably. You can use X * info.ARK to denote a X ARK

# How to connect to the ark-node
CONNECTION = {
    'HOST': 'localhost',
    'DATABASE': 'ark_mainnet',
    'USER': 'postgres',
    'PASSWORD':  'Dwl1ml12_3#',
}

# Who are we: the delegate's info.
DELEGATE = {
    'PUBKEY'      : None,
    'ADDRESS'     : 'example',
    'PASSPHRASE'  : None,
    'REWARDWALLET': None,
    'REWARD_SMARTBRIDGE': '',
    }

CALCULATION_SETTINGS = {
    'STARTBLOCK_CALCULATION': 0,

}


# How are fees calculated.
SENDER_SETTINGS = {
    # at calculation, wallet has to be a current voter
    'REQUIRE_CURRENT_VOTER': True,
    # The default share ratio
    'DEFAULT_SHARE': 1,
    # startblock calculation

    # any balance above max balance or below min balance is not taken in the
    # calculation (the ark is divided amongst voters and delegate)
    # so if MAX_BALANCE == 200k and a voter has
    # 300k, it is counted as 200K.
    # If a voter has 1 Ark, and MIN_BALANCE == 2 Ark, it is counted as 0 Ark
    'MIN_PAYOUT_BALANCE'           : 0,
    'COVER_TX_FEES'                : False,

    # At the end of the personal message a tag could be included for
    # administrative purposes
    # Example: 'Thanks for voting! ::VOTINGFEE::
    'PERSONAL_MESSAGE': None,
    # min amount of seconds between a payout
    'WAIT_TIME': 0,
    'WAIT_TIME_REWARD': 0,

}

# Blacklisted voters: whom do we never wish to pay out. Their Ark is divided over all other voters + delegate
# format is a list
BLACKLIST = None

# Like blacklist, except delegate gets to keep the ark (not automatically added to delegate share)
DARKLIST = None

# preset amounts to be sent. format is a dict with address: amount. amount is in arksatoshis (10^8 as = 1 ark)
HARD_EXCEPTIONS = None

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