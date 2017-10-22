# PayoutScriptArk
PayoutScript for Ark delegates

WARNING: Not all features are specified in the payout script yet. Do not use it
if you cannot review the code yourself, although it is functional for daily,
weekly and monthly payouts and uses accurate true-blockweight calculations

## How to use the payout script?

You will need access to the Ark node Postgresql database. The payout script
accesses it. In order to provide access for this script to the database, you
can edit /etc/postgresql/9.5/main/pg_hba.conf and replace md5 by trust. Beware
that now anyone can access your database and edit its contents, so make sure to
either not share the DB, or if you are more experienced, make a new user with
only SELECT privileges.

Next edit config.py file with your personal details such as who you are
(delegate's public key etc.) and how you want to pay out your voters. You can
also blacklist voters or set special payout schemes on a per-voter basis in
EXCEPTIONS.

Also make sure to review all paths (directories) and make them suitable for
your setup. The sample configuration is built up as follows:

*  The home directory of the user is /home/ark
*  Payouts are written to /home/ark/payouts
*  Payout files that fail to send are moved to /home/ark/failedpayouts
*  Actions are logged to /tmp/ark.log

Next, have a look at `runpaymentcycle`. This is a bash script to tie it all
together. If necessary, change the configuration variables at the top. Then you
can run the cycle.

## Your first payment cycle

The suggested way to test your first payment cycle, is to edit `config.py` and
to set `PAYOUTSENDER_TEST` to `True`. That will cause the sender only to show
what would be sent, but not to actually send out any payments.

## Random Tips

Want to develop on windows and access a node through this script? Use an SSH
tunnel: http://realprogrammers.com/how_to/set_up_an_ssh_tunnel_with_putty.html
