#!/usr/bin/env python
#
#  Copyright (c) 2010, Vinod Kurup (vinod@kurup.com)
#
#  license: GNU GPL
#

import subprocess
import re
from datetime import date
# Objective: 
#   Create the ledger entry to properly sell a stock. Provide some data
#   about the performance of that stock.
#
#   Ask user for symbol, sell date, sell price, #shares to sell
#   clarify symbol if it exists in more than 1 account
#   Find the currently held # of shares, cost basis
#   calculate the $gain and %gain
#   create the ledger entry for the sell

def sell_stock(symbol, sell_date, sell_price, shares):
    """Create the ledger entry to sell a stock.
    
    Arguments:
    - `symbol`:
    - `sell_date`:
    - `sell_price`:
    - `shares`:
    """
    pass
 
def get_data():
    """Get the input data from the user
    """
    symbol = raw_input("Symbol: ")
    sell_price = 18.60 # fixme

    # default to today
    now = date.today()
    sell_date = now.strftime("%Y/%m/%d")

    proc = subprocess.Popen(["ledger","-n","bal",'^Assets.*:%s$' % (symbol)],stdout=subprocess.PIPE, )
    ledger_result = proc.communicate()[0].splitlines()

    for line in ledger_result:
        line.strip()
        #filter lines that don't have the symbol in them (commission)
        # fixme: deal with multiple lines (stock in >1 account)
        pattern = '[0-9\.]+'
        if line.find(symbol) != -1 :
            shares = int(re.findall(pattern, line)[0])
            pattern = 'Assets.*:+.*'
            account = re.findall(pattern, line)[0]
        else:
            buy_commission = float(re.findall(pattern, line)[0])

    proc = subprocess.Popen(["ledger","-B","reg",'^%s$' % (account)],stdout=subprocess.PIPE, )
    ledger_result = proc.communicate()[0].splitlines()

    # now get buy_date and buy_price
    for line in ledger_result:
        line.strip()
        #filter lines that don't have the word "BUY"
        if line.find("BUY") != -1 :
            pattern = '\d{4}/\d{2}/\d{2}'
            buy_date = re.findall(pattern, line)[0]
            pattern = '\$[\d,\.]+'
            buy_cost = re.findall(pattern, line)[0]
            buy_cost = buy_cost.replace("$","")
            buy_cost = float(buy_cost.replace(",",""))
        else:
            pass

    buy_price = buy_cost / shares
    print "Selling %d shares of %s (account %s) on %s" % (shares, symbol, account, sell_date)
    print "Buy commission was %.2f" % (buy_commission)
    print "Buy date was %s" % (buy_date)
    print "Buy cost was %s" % (buy_cost)
    print "Buy price was %.2f" % (buy_price)
    print "Sell price is %.2f" % (sell_price)

    print """%s  SELL %s
    %s  -%d @ $%.2f
    %s   %d @ $%.2f
    %s  -%d @ $%.2f
    %s  $-%.2f ; buy commission
    Income:Capital Gains:ST  $7.07 ; sell commission
    %s  $%.2f
    Income:Capital Gains:ST""" % (sell_date,symbol,account,shares,buy_price,account,shares,sell_price,account,shares,sell_price,account,buy_commission,account,shares*sell_price)

#sell_date = raw_input("Sell date: ")
#sell_price = raw_input("Sell price: ")
#sell_shares = raw_input("# of shares: ")

# run: ledger -n bal '^Assets.*:symbol$'
# gives this output
#               $7.00
#              265 GE  Assets:Investments:Scottrade:SEP:GE
#proc = subprocess.Popen(["ledger","-n","bal",'Assets.*:%s' % (symbol)],stdout=subprocess.PIPE, )
#a = proc.communicate()[0]

#validate symbol, sell_date, sell_price, sell_shares
#print "We sold %s shares of %s on %s for $%s" % (sell_shares,symbol,sell_date,sell_price)

#print a

if __name__ == "__main__":
    get_data()
