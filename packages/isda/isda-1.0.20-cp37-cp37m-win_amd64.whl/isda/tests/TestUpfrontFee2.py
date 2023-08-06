import unittest
import datetime
import uuid

from isda.isda import compute_isda_upfront, average, cds_all_in_one_exclude_ir_tenor_dates
from isda.imm import imm_date_vector


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

        self.is_rofr = 1
        self.swap_rates = [0.023073, 0.02604, 0.02787, 0.031397, 0.03403, 0.033118, 0.031109, 0.029499, 0.028489,
                           0.027959, 0.02764, 0.02746, 0.0274, 0.02745, 0.027739, 0.028060, 0.027899, 0.027069,
                           0.026170]
        self.swap_tenors = ['1M', '2M', '3M', '6M', '1Y', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '8Y', '9Y', '10Y', '12Y',
                            '15Y', '20Y', '25Y', '30Y']

        # economics of trade
        self.coupon = 100.0
        self.trade_date = '22/08/2022'
        self.effective_date = '23/08/2022'
        self.accrual_start_date = '22/06/2022'
        self.maturity_date = '20/09/2027'
        self.notional = 10.0
        self.is_buy_protection = 0  # only ever buy or sell protection!
        self.verbose = 0
        self.tenor_list = [0.5, 1, 2, 3, 4, 5, 7, 10]

        # used to generate and shock roll dataset
        self.spread_roll_tenors = []
        self.scenario_shifts = []

    def tearDown(self):
        pass

    def test_compute_isda_upfront(self):
        """
        Process finished with exit code 0
        credit_spread 45.0 recovery_rate 0.4 upfront_charge: 27573.02664720266 pv_clean (clean price) 102.57219208021354 dirty_price (Cash Settlement Amount) 27471.92080213547 ai 1750.0000000000016
        credit_spread 55.0 recovery_rate 0.4 upfront_charge: 22808.98548867634 pv_clean (clean price) 102.09576148061264 dirty_price (Cash Settlement Amount) 22707.614806126363 ai 1750.0000000000016
        credit_spread 65.0 recovery_rate 0.4 upfront_charge: 18084.047153034346 pv_clean (clean price) 101.62324051685925 dirty_price (Cash Settlement Amount) 17982.40516859251 ai 1750.0000000000016
        credit_spread 75.0 recovery_rate 0.4 upfront_charge: 13397.884539847697 pv_clean (clean price) 101.15459650030917 dirty_price (Cash Settlement Amount) 13295.965003091651 ai 1750.0000000000016
        credit_spread 85.0 recovery_rate 0.4 upfront_charge: 8750.17330450548 pv_clean (clean price) 100.68979701753237 dirty_price (Cash Settlement Amount) 8647.970175323704 ai 1750.0000000000016
        average execution (23.8,)
        """

        self.sdate = datetime.datetime(2022, 8, 23)
        self.value_date = self.sdate.strftime('%d/%m/%Y')

        self.imm_dates = [f[1] for f in imm_date_vector(
            start_date=self.sdate, tenor_list=self.tenor_list)]

        # simulate an index with 125 names;;
        self.credit_spread_list = [45 / 10000]
        self.recovery_rate_list = [0.4]

        self.swapFloatingDayCountConvention = 'ACT/360'
        self.swapFixedDayCountConvention = 'ACT/360'
        self.swapFixedPaymentFrequency = '1Y'
        self.swapFloatingPaymentFrequency = '1Y'

        unique_filename = str(uuid.uuid4())
        self.holiday_filename = f'{unique_filename}.dat'
        self.holiday_list = [16010101, 20180320, 20181220]

        def save_to_file(*holiday_list):
            with open(self.holiday_filename, mode='wt', encoding='utf-8') as myfile:
                for lines in holiday_list:
                    myfile.write('\n'.join(str(line) for line in lines))
                    myfile.write('\n')

        # just for measuring performance

        save_to_file(self.holiday_list)

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
                                     self.is_rofr,
                                     self.holiday_filename,
                                     self.swapFloatingDayCountConvention,
                                     self.swapFixedDayCountConvention,
                                     self.swapFixedPaymentFrequency,
                                     self.swapFloatingPaymentFrequency,
                                     self.verbose)

            upfront_charge, status, duration_in_milliseconds = f

            # spread curve download from markit
            self.credit_spreads = [credit_spread] * 8
            self.credit_spread_tenors = ['6M', '1Y', '2Y', '3Y', '4Y', '5Y', '7Y', '10Y']

            f = cds_all_in_one_exclude_ir_tenor_dates(self.trade_date,
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
                                                      self.credit_spreads,
                                                      self.credit_spread_tenors,
                                                      self.spread_roll_tenors,
                                                      self.imm_dates,
                                                      self.scenario_shifts,
                                                      self.verbose)

            pv_dirty, pv_clean, ai, cs01, dv01, duration_in_milliseconds = f[0]

            wall_time_list.append(float(duration_in_milliseconds))
            print(f"credit_spread {credit_spread * 10000.} "
                  f"recovery_rate {recovery_rate} "
                  f"upfront_charge: {100 + abs(upfront_charge * 1e6)} "
                  f"pv_clean (clean price) {100 + abs(pv_clean * 10)} "
                  f"dirty_price (Cash Settlement Amount) {pv_dirty * 1e6} "
                  f"ai {ai * 1e6} ")

        a = [wall_time_list]
        print("average execution {0}".format(average(a)))


if __name__ == '__main__':
    unittest.main()
