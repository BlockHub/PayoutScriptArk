# PayoutScriptArk
PayoutScript for Ark delegates

WARNING: Not all features are specified in the payout script yet. Do not use it if you cannot review the code yourself, although it is functional for daily, weekly and monthly payouts and uses accurate true-blockweight calculations

How to use the payout script?

The payout script directly queries a node database, meaning you first need to make the nodes Postgresql DB accessible to other programs. The easiest way to accomplish that is to go to etc/postgresql/9.5/main/. There edit your pg_hba.conf, replacing peer and both occurences of md5 by trust. Beware that now anyone can access your database and edit its contents, so make sure to either not share the DB, or if you are more experienced, make a new user with only SELECT privileges.

Next edit the config file with your personal details (taxes and blacklisted addresses)

Want to develop on windows and access a node through this script? Use an SSH tunnel: http://realprogrammers.com/how_to/set_up_an_ssh_tunnel_with_putty.html
