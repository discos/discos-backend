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

