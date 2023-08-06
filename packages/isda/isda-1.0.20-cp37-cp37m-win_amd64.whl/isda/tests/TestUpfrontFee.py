import unittest
import datetime

from isda.isda import compute_isda_upfront, average


class MyTestCase(unittest.TestCase):
    """
        Testcase that has been reconciled with output from MarkIT partners online calculator and
        separate ISDA source; these figures are accurate to 11 decimal places and battle tested
        enough to be useful for more than just indicative risk.

        i) test coverage needs to be extended to handle cases over weekends & holidays
        ii) for now the coverage is a simple buy/sell protection flat spread trade

    """

    __name__ = "MyTestCase"

    def setUp(self):
        # available from markit swap feed
        self.swap_rates = [-0.00369, -0.00340, -0.00329, -0.00271, -0.00219, -0.00187, -0.00149, 0.000040, 0.00159,
                           0.00303, 0.00435, 0.00559, 0.00675, 0.00785, 0.00887]
        self.swap_tenors = ['1M', '2M', '3M', '6M', '9M', '1Y', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '8Y', '9Y', '10Y']

        # economics of trade
        self.coupon = 100.0
        self.trade_date = '12/12/2014'
        self.effective_date = '13/12/2014'
        self.accrual_start_date = '20/9/2014'
        self.maturity_date = '20/12/2019'
        self.notional = 1.0
        self.is_buy_protection = 1  # only ever buy or sell protection!
        self.verbose = 1

    def tearDown(self):
        pass

    def test_compute_isda_upfront(self):
        """ method to specifically test performance to price an index cds with 125 names """

        self.sdate = datetime.datetime(2018, 1, 8)
        self.value_date = self.sdate.strftime('%d/%m/%Y')

        # simulate an index with 125 names;;
        self.credit_spread_list = [10/10000., 15/10000., 20/10000.]
        self.recovery_rate_list = [0.2, 0.25, 0.4]

        wall_time_list = list()
        for credit_spread, recovery_rate in zip(self.credit_spread_list, self.recovery_rate_list):
            f = compute_isda_upfront(self.trade_date,
                                     self.effective_date,
                                     self.maturity_date,
                                     self.value_date,
                                     self.accrual_start_date,
                                     recovery_rate,
                                     self.coupon,
                                     self.notional,
                                     self.is_buy_protection,
                                     self.swap_rates,
                                     self.swap_tenors,
                                     credit_spread,
                                     self.verbose)

            upfront_charge, status, duration_in_milliseconds = f
            wall_time_list.append(float(duration_in_milliseconds))
            print(f"upfront_charge: {upfront_charge}")

        a = [wall_time_list]
        print("average execution {0}".format(average(a)))


if __name__ == '__main__':
    unittest.main()
