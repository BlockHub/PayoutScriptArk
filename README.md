# PayoutScriptArk: PayoutScript for Ark delegates

> WARNING: Not all features are specified in the payout script yet. Do
> not use it if you cannot review the code yourself, although it is
> functional for daily, weekly and monthly payouts and uses accurate
> true-blockweight calculations.

## How to use the payout script?

The payout scripts will need access to an Ark node Postgresql database. this
can be located on the local host or accessed via the network. You will need to
define how to connect to the database in `config.py`: the provided example
connects to a database on the local machine.

Also in `config.py` set your personal details such as who you are (delegate's
public key etc.) and how you want to pay out your voters. You can also
blacklist voters or set special payout schemes on a per-voter basis in
`EXCEPTIONS`. The configuration file has comments that mostly clarify what a
setting does. Just follow the examples. (Blacklisting voters is at the moment
used to exclude delegates from the payment cycle. These have a transaction
history that needs to be handled differently than 'standard' voters; this is
work in progress.)

Also make sure to review all paths (directories) and make them suitable for
your setup. The sample configuration is built up as follows:

*  The home directory of the user is `/home/ark`
*  Payouts are written to `/home/ark/payouts`
*  Payout files that fail to send are moved to `/home/ark/failedpayouts`
*  Actions are logged to `/tmp/ark.log`

Next, have a look at `runpaymentcycle`. This is a bash script to tie it all
together. If necessary, change the configuration variables at the top. Then you
can run the cycle.

## Your first payment cycle

The suggested way to test your first payment cycle, is to edit `config.py` and
to set `PAYOUTSENDER_TEST` to `True`. That will cause the sender only to show
what would be sent, but not to actually send out any payments.

Now run the first phase: `runpaymentcycle calculator`. This will create a
bunch of payment files and save its logging to `/tmp/ark.log` (unless you have
changed the logfile in `config.py`). Review the logfile for correctness.

Now run the second phase: `runpaymentcycle sender`. This will pick up the
payment files and again create logging, but nothing will be sent. Again,
review the logging for correctness.

Now optionally run `runpaymentcycle reporter`. It will report a lot of active
payments (to be sent), because the sender doesn't actually send anything with
`PAYOUTSENDER_TEST` set to `True`.

Once you are satisfied and want to try for real:

*  Change `config.py` and set the test flag `PAYOUTSENDER_TEST` to `False`.
*  Manually remove previously generated payment files:
   `rm -r /home/ark/payouts` (or whatever you have configured in `config.py`
   as the `PAYOUTDIR`).
*  Manually remove previous failed attempts:
   `rm -r /home/ark/failedpayouts` (or whatever you have configured in
   `config.py` as the `PAYOUTFAILDIR`).
*  Redo the `runpaymentcycle` steps.

## Automating the Payments

Using `runpaymentcycle` in `cron` is the most obvious way to automate running
the payment cycles. Depending on your payout frequency you may want to run
`runpaymentcycle` daily, weekly or even monthly. The following examples assume
a daily run; adapt `cron`s time settings accordingly if you want different
settings.

### Initial `crontab`

The `12` in the example below defines the minutes, the `3` defines the hour (3
AM). The asterisks mean that the command should be run every day of the month,
every month, every day of the week. 12 minutes past 3 is chosen at random.
(Folks use 0 0, which means that the Internet gets swamped with traffic at
midnight. Don't do that.)

So, run `crontab -e` to edit your `cron` definition, and enter something like
what's shown below:

``` shell
# Set your mail address
MAILTO=joe@someaddress.tld

12 3 * * * /home/ark/PayoutScriptArk/runpaymentcycle all
```

This will possibly generate a lot of mails; even debugging output (which
normally goes to the standard output stream and ends up in the mail). Argument
`all` causes `runpaymentcycle` to run the calculator, sender and reporter.

### Less Spam

Once you are satisfied that this works, add `>/dev/null` to the invocation of
`runpaymentcycle`. This will discard the standard output, but any warnings or
errors (which go to the standard error stream) will still be mailed. This
means that when all goes well and no warnings or errors occur, you don't get
mail. No news is good news, right.

```shell
# Set your mail address
MAILTO=joe@someaddress.tld

12 3 * * * /home/ark/PayoutScriptArk/runpaymentcycle all >/dev/null
```

### Not Running the Reporter During Every Cycle

If you are even more confident, you can stop running the reporter during each
cycle, but run it e.g. just weekly. Argument `both` causes `runpaymentcycle`
to run only the calculator and sender.

```shell
# Set your mail address
MAILTO=joe@someaddress.tld

12 3 * * * /home/ark/PayoutScriptArk/runpaymentcycle both   >/dev/null
12 6 * * 0 /home/ark/PayoutScriptArk/runpaymentcycle report >/dev/null
```

The 0 in the invocation of the reporter stands for the day of the week, 0 being
Sunday.

### Not Running the Reporter At All

When all is stable, you can even comment out the above invocation to run the
reporter. Remember; if warnings or errors are generated, they will be sent
anyway. If that happens, you can always log in to your Unix box and run the
reporter by hand.

## Debugging Failed Payments

When the payout sender (invoked by `runpaymentcycle sender`) cannot deliver a
payment, then the payment file is moved to the `PAYOUTFAILDIR`, e.g.
`/home/ark/failedpayouts`. You can display the file contents by running
`runpaymentcycle displayer <filenames>`, e.g.:

```shell
runpaymentcycle displayer /home/ark/failedpayouts/*
```

If you suspect a transient error (e.g., the network was down and
payments could not be sent), then just move the files from the failure
directory to the to-be-sent directory, and run the sender again
(adjust accordingly if you have configured other directories `PAYOUTDIR` or
`PAYOUTFAILDIR`):


``` shell
mv /home/ark/failedpayouts/* /home/ark/payouts/
/home/ark/PayoutScriptArk/runpaymentcycle sender
```

## Random Tips

*  Want to develop on windows and access a node through this script? Use an SSH
   tunnel:
   http://realprogrammers.com/how_to/set_up_an_ssh_tunnel_with_putty.html
*  Having trouble connecting to a database on your local machine? You can edit
   `/etc/postgresql/9.5/main/pg_hba.conf` and replace `md5` by `trust`.  Beware
   that now anyone can access your database and change its contents, so make
   sure to either not share the access, or if you are more experienced, make a
   new user with only `SELECT` privileges. See the Postgresql documentation for
   more info; an in-depth discussion is out of scope here.
