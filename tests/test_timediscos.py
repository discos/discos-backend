
#
#
#   Copyright 2015 Marco Bartolini, bartolini@ira.inaf.it
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

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

    def test_get_acs_now(self):
        expected = self.now * timediscos.CENTINANOSECONDS
        now = timediscos.get_acs_now()
        self.assertAlmostEqual(
            expected, now.unix * timediscos.CENTINANOSECONDS, delta=1000
        )


if __name__ == "__main__":
    unittest.main()
