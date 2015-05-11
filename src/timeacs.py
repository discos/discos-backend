from decimal import Decimal

from astropy.time import TimeUnix, TimeFromEpoch, TimeFormat, Time
import astropy._erfa as erfa

CENTINANOSECONDS = 10000000

class TimeAcs(TimeUnix):
    """
    Acs Time: centinanoseconds from 1970-01-01 00:00:00 UTC
    """
    name = 'acs'
    unit = 1.0 / (erfa.DAYSEC * CENTINANOSECONDS)

    def __init__(self, val1, val2, scale, precision,
                 in_subfmt, out_subfmt, from_jd=False):
        super(TimeAcs, self).__init__(val1, val2, scale, 7,
                                      in_subfmt, out_subfmt, from_jd)


def parse_unix_time(unix_timestamp_string):
    int_timestamp = int(Decimal(unix_timestamp_string) * CENTINANOSECONDS)
    return Time(int_timestamp,
                format = 'acs',
                standard = 'utc',
                precision = 7)


