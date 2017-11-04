# PayoutScriptArk
PayoutScript for Ark delegates, example of using arkdbtools

This payoutscript uses the arkdbtoolsfunctions to calculate trueblockweight and then uses Core.payoutsender to send the transactions.

To setup a node and configure it, check the arkdbtools repo, whcih also contains some documentation on the settings.

The bashscript has hardcoded directories. It expects the following:

virtualenvironment: /home/ark/PayoutScriptArk/venv/bin/activate
plugandplay location: /home/ark/PayoutScriptArk/plugandplay.py

So basically edit that file, or create a user called Ark:

```sh
sudo adduser ark
usermod -aG sudo ark
```

Then clone this repo:

```sh
cd
git clone https://github.com/Nijmegen-Consultancy-Group/PayoutScriptArk.git
cd PayoutScriptArk
```

Next get python 3.6 and a virtual environment:

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
sudo pip3.6 install virtualenv
```

And then create the virtual environment:
```sh
virtualenv venv -p python3.6
```

And start the venv:
```sh
source venv/bin/activate
```

Now we need to pip install the requirements. I have been a bit careless with my dev environment, so you are getting some packages that you
don't need. I will later update requirements.txt to reflect what you actually need.

```sh
pip install pip install -r requirements.txt
```

So everything should be setup. Check the config and enter your settings. Leave the secret/passphrase for now. 

```python
DELEGATE = {
    'PUBKEY'      : None,
    'ADDRESS'     : None,
    'PASSPHRASE'  : None,
    'REWARDWALLET': None,
    }
    
...

PAYOUTCALCULATOR_TEST = True
PAYOUTSENDER_TEST = True
```

Next edit plugandplay.py with your connection parameters. The function is inside main() (I will change this later to be edited in config.py):

```python
ark.set_connection(
        host='localhost',
        database='ark_mainnet',
        user='ark',
        password=None)
```
Now we should be able to do a test run and see if everything works.

```sh
python plugandplay.py
```

This should take approximately 2 minutes.

Lets check the logs:

```sh
nano /tmp/payoutscriptark.log
```

Check the logs. Txparametererros are fine. They are produced when a voter's balance is below the threshold, or if he has had a payout recently
the sender then skips these until they have accumulated enough Ark.

If you are okay with the numbers and everything looks good, you can enter your passhrase:

```sh
nano /home/ark/PayoutScriptArk/config.py 
```

```python
DELEGATE = {
...
'PASSPHRASE'  : 'yourpasshprase here',
}

PAYOUTCALCULATOR_TEST = False
PAYOUTSENDER_TEST = False

SECRET = 'string'
```

If you run the script now, it will recalculate the payments and transfer the Ark.

If everything worked out fine, you could easily automate the script. I recommend running the script at a certain time every day, and since
some errors could occur, run it a couple of times, with 30  minute intervals (to make sure your node has processed the transactions)


```sh
crontab -e
```
Cron is a daemon used to run scripts at certain timeintervals. Read the documentation here: http://www.nncron.ru/help/EN/working/cron-format.htm

In this example we run the script every day at 17:00, then again at 18:00, 19:00, 20:00 and 21:00 P.M

```sh
00 17 * * * /home/ark/PayoutScriptArk/runpayments
00 18 * * * /home/ark/PayoutScriptArk/runpayments
00 19 * * * /home/ark/PayoutScriptArk/runpayments
00 20 * * * /home/ark/PayoutScriptArk/runpayments
00 21 * * * /home/ark/PayoutScriptArk/runpayments
```

The script does not charge a fee whatsover. If you use it, consider donating to 'AJwHyHAArNmzGfmDnsJenF857ATQevg8HY'













