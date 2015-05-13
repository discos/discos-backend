import unittest
import time
from decimal import Decimal

from discosbackend import timediscos
from astropy.time import Time

class TestTimeDiscos(unittest.TestCase):

    def setUp(self):
        self.now = time.time()

    def test_astropy_conversion(self):
        dt = Time(self.now * timediscos.CENTINANOSECONDS,
                 format="discos")
        ut = Time(self.now, format="unix")
        self.assertEqual(ut.datetime, dt.datetime)

    def test_astropy_constructor(self):
        dt = Time(self.now * timediscos.CENTINANOSECONDS,
                 format="discos")
        self.assertAlmostEqual(self.now, dt.unix, places=6)

    def test_unix_parsing_function(self):
        now = Decimal(self.now).to_eng_string() 
        dt = timediscos.parse_unix_time(now)
        self.assertAlmostEqual(self.now, dt.unix, places=6)
