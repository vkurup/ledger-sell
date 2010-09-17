#!/usr/bin/env python
#
#  Copyright (c) 2010, Vinod Kurup (vinod@kurup.com)
#
#  license: GNU GPL
#

import unittest
import ledger_sell

class LedgerSellTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_returns_proper_output(self):
        output = ledger_sell.create_sell_txn("2010/09/16", "GE", "Assets:Investments:BrokerA", 100, 10.03, 12.15, 7.00, 7.08, "Income:Capital Gains:ST")
        expected_output = """2010/09/16 SELL GE
    Assets:Investments:BrokerA:GE  -100 GE @ $10.03
    Assets:Investments:BrokerA:GE  100 GE @ $12.15
    Assets:Investments:BrokerA:GE  -100 GE @ $12.15
    Assets:Investments:BrokerA:GE  $-7.00  ; buy commission
    Income:Capital Gains:ST  $7.08  ; sell commission
    Assets:Investments:BrokerA  $1,207.92
    Income:Capital Gains:ST
"""
        self.assertEquals(output, expected_output)
        
if __name__ == "__main__":
    unittest.main()
