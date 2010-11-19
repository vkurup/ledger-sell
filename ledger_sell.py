#!/usr/bin/env python
#
#  Copyright (c) 2010, Vinod Kurup (vinod@kurup.com)
#
#  license: GNU GPL
#

import subprocess
import re
from datetime import date
import locale

locale.setlocale(locale.LC_ALL, "")

# Objective: 
#   Create the ledger entry to properly sell a stock. Provide some data
#   about the performance of that stock.
#
#   Ask user for symbol, sell date, sell price, #shares to sell
#   clarify symbol if it exists in more than 1 account
#   Find the currently held # of shares, cost basis
#   calculate the $gain and %gain
#   create the ledger entry for the sell

def create_sell_txn(sell_date, symbol, parent_account, shares, buy_price, sell_price, buy_comm, sell_comm, cap_gains_account):
    """Given all of the inputs, create a ledger sell transaction.
    
    Arguments:
    - `sell_date`:
    - `symbol`:
    - `parent_account`:
    - `shares`:
    - `buy_price`:
    - `sell_price`:
    - `buy_comm`:
    - `sell_comm`:
    - `cap_gains_account`:
    """
    proceeds = locale.format('%.2f', sell_price * shares - sell_comm, True)

    return """{sell_date} SELL {symbol}
    {parent_account}:{symbol}  -{shares} {symbol} @ ${buy_price}
    {parent_account}:{symbol}  {shares} {symbol} @ ${sell_price}
    {parent_account}:{symbol}  -{shares} {symbol} @ ${sell_price}
    {parent_account}:{symbol}  $-{buy_comm:.2f}  ; buy commission
    {cap_gains_account}  ${sell_comm:.2f}  ; sell commission
    {parent_account}  ${proceeds}
    {cap_gains_account}
""".format(**vars())

def calculate_txn_items(symbol, sell_price, account=-1, shares=-1, sell_comm=7.00, sell_date=-1):
    """Calculate all the items we need to create the transaction.
    
    Arguments:
    - `symbol`: required. Symbol of position we're selling
    - `sell_price`: required. Price that we sold at.
    - `account`: optional. Needed if stock is held in multiple accounts (FIXME)
    - `shares`: optional. If not provided, assume we're selling all.
    - `sell_comm`: optional. Defaults to $7.00 (scottrade)
    - `sell_date`: optional. Defaults to today.
    """
    if sell_date == -1:
        sell_date = date.today().strftime("%Y/%m/%d")

    if account != -1:
        pass #fixme
    
    if shares != -1:
        pass #fixme

    # FIXME: adjust commission to include SEC fee

    (shares, account) = ledger_balance_data(symbol)
    (buy_date, buy_cost, buy_comm) = ledger_buy_data(account)
    buy_price = buy_cost / shares
    parent_account = account.rsplit(":",1)[0] # everything but the symbol

    print create_sell_txn(sell_date, symbol, parent_account, shares, buy_price, sell_price, buy_comm, sell_comm, "Income:Capital Gains:ST")
    
def ledger_balance_data(symbol):
    """Return tuple of data (shares, account) for a specific symbol
    
    Arguments:
    - `symbol`:
    """
    proc = subprocess.Popen(["ledger","-n","bal",'^Assets.*:%s$' % (symbol)],stdout=subprocess.PIPE, )
    ledger_result = proc.communicate()[0].splitlines()

    for line in ledger_result:
        line.strip()
        #filter lines that don't have the symbol in them (commission)
        # fixme: deal with multiple lines (stock in >1 account)
        if line.count(symbol):
            pattern = '[0-9\.]+'
            shares = int(re.findall(pattern, line)[0])
            pattern = 'Assets.*:+.*'
            account = re.findall(pattern, line)[0]
    return (shares, account)

def ledger_buy_data(account):
    """Return tuple of data (buy_date, buy_cost, buy_comm) for a specific symbol
    
    Arguments:
    - `symbol`:
    """
    proc = subprocess.Popen(["ledger","-B","reg",'^%s$' % (account)],stdout=subprocess.PIPE, )
    ledger_result = proc.communicate()[0].splitlines()

    # now get buy_date, buy_price, and buy_comm
    for line in ledger_result:
        line.strip()
        #filter lines that don't have the word "BUY"
        if line.count("BUY"):
            pattern = '\d{4}/\d{2}/\d{2}'
            buy_date = re.findall(pattern, line)[0]
            pattern = '\$[\d,\.]+'
            buy_cost = re.findall(pattern, line)[0]
            buy_cost = buy_cost.replace("$","")
            buy_cost = float(buy_cost.replace(",",""))
        else:
            pattern = '[0-9\.]+'
            buy_comm = float(re.findall(pattern, line)[0])
    return (buy_date, buy_cost, buy_comm)
    

if __name__ == "__main__":
    #fixme: validate
    symbol = raw_input("Symbol: ")
    sell_price = float(raw_input("Sell price: $"))
    calculate_txn_items(symbol, sell_price)
