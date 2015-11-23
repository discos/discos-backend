
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

from decimal import Decimal

from astropy.time import TimeUnix, Time
import astropy._erfa as erfa
import time

CENTINANOSECONDS = 10000000

class TimeDiscos(TimeUnix):
    """
    Acs Time: centinanoseconds from 1970-01-01 00:00:00 UTC
    """
    name = 'discos'
    unit = 1.0 / (erfa.DAYSEC * CENTINANOSECONDS)

    def __init__(self, val1, val2, scale, precision,
                 in_subfmt, out_subfmt, from_jd=False):
        super(TimeDiscos, self).__init__(val1, val2, scale, 7,
                                      in_subfmt, out_subfmt, from_jd)


def parse_unix_time(unix_timestamp_string):
    int_timestamp = int(Decimal(unix_timestamp_string) * CENTINANOSECONDS)
    return Time(int_timestamp,
                format = 'discos',
                scale = 'utc',
                precision = 7)

def get_acs_now():
    return Time(time.time() * CENTINANOSECONDS, format="discos")

def unix_to_acs_time(unix_timestamp):
    return Time(unix_timestamp * CENTINANOSECONDS, format="discos")

