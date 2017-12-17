import arkdbtools.dbtools
import arkdbtools.config
import config
address = ''



arkdbtools.dbtools.set_connection(
                        host='localhost',
                        database='ark_mainnet',
                        user='postgres',
                        password='Dwl1ml12_3#')

current_balance = arkdbtools.dbtools.Address.balance(address)


payouts = arkdbtools.dbtools.Delegate.trueshare(del_address=address)


to_be_paid = 0
for i in payouts:
    to_be_paid += (payouts[i]['share'] + arkdbtools.config.TX_FEE)


print(current_balance)
print(to_be_paid)
print(current_balance-to_be_paid/arkdbtools.config.ARK)