import unittest

from pwiqf import option_pricing


class OptionPricingTest(unittest.TestCase):

    def test_get_eu_price_with_binomial(self):
        self.assertAlmostEqual(
            option_pricing.get_price_with_binomial('C', 'eu', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False),
            6.1344724,
            places=6)
        self.assertAlmostEqual(
            option_pricing.get_price_with_binomial('P', 'eu', 100, 0.2, 0.1, 100, 1 / 12, 4, print_details=False),
            3.352622,
            places=6)

