
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

import time
import random
import re
from twisted.internet import reactor
from discosbackend.handlers import HandlerException


class BackendError(HandlerException):
    pass


class BackendSimulator:
    def __init__(self):
        self.status_string = "ok"
        self.acquiring = False
        self.configuration_string = "unconfigured"
        self.integration = 0
        self._waiting_for_start_time = False
        self._startID = None
        self._waiting_for_stop_time = False
        self._stopID = None
        self._valid_conf_re = re.compile("^[a-z]")
        self._sections = {}
        self._max_bandwidth = 2000
        self._max_sections = 5
        self._filename = ""
        self.interleave = 0
        self.current_sections = range(0, self._max_sections)
        self.shift = 0

    def status(self):
        return (
            self._get_time(),
            self.status_string,
            1 if self.acquiring else 0
        )

    def get_tpi(self):
        return [random.random() * 100, random.random() * 100]

    def get_tp0(self):
        return [0, 0]

    def get_configuration(self):
        return [self.configuration_string]

    def set_configuration(self, conf_name):
        if not self._is_valid_configuration(conf_name):
            raise BackendError("invalid configuration")
        # here you should perform actual hardware configuration
        self.configuration_string = conf_name

    def get_integration(self):
        return [self.integration]

    def set_integration(self, integration):
        self.integration = integration

    def time(self):
        return [self._get_time()]

    def start(self, timestamp=None):
        if not timestamp:
            self._start_now()
        else:
            self._start_at(timestamp.unix)

    def stop(self, timestamp=None):
        if not timestamp:
            self._stop_now()
        else:
            self._stop_at(timestamp.unix)

    def set_section(
            self,
            section,
            start_freq,
            bandwidth,
            feed,
            mode,
            sample_rate,
            bins):
        if section > self._max_sections and not section == "*":
            raise BackendError(
                f"backend supports {self._max_sections} sections"
            )
        if not bandwidth == "*" and int(bandwidth) > self._max_bandwidth:
            raise BackendError(
                f"backend maximum bandwidth is {self._max_bandwidth}"
            )
        self._sections[section] = (
            start_freq,
            bandwidth,
            feed,
            mode,
            sample_rate,
            bins
        )

    def cal_on(self, interleave):
        self.interleave = interleave

    def set_filename(self, filename):
        self._filename = filename

    def convert_data(self):
        pass

    def set_enable(self, feed1, feed2):
        if feed1 not in range(int(self._max_sections / 2)):
            raise BackendError("feed1 out of range")
        if feed2 not in range(int(self._max_sections / 2)):
            raise BackendError("feed2 out of range")
        self.current_sections = [
            feed1 * 2,
            feed1 * 2 + 1,
            feed2 * 2,
            feed2 * 2 + 1
        ]

    def end_schedule(self):
        pass

    def park(self):
        pass

    def set_shift(self, shift):
        self.shift = shift

    def _get_time(self):
        # should ask the backend hardware clock
        return time.time()

    def _is_valid_configuration(self, configuration_name):
        return self._valid_conf_re.match(configuration_name)

    def _start_at(self, timestamp):
        if timestamp < time.time():
            raise BackendError("starting time already elapsed")
        if self._waiting_for_start_time:
            self._startID.cancel()
        self._waiting_for_start_time = True
        self._startID = reactor.callLater(
            timestamp - time.time(),
            self._start_now
        )

    def _start_now(self):
        if self.acquiring:
            raise BackendError("already acquiring")
        self._waiting_for_start_time = False
        self.acquiring = True

    def _stop_now(self):
        if not self.acquiring:
            raise BackendError("not acquiring")
        self._waiting_for_start_time = False
        self._waiting_for_stop_time = False
        self.acquiring = False

    def _stop_at(self, timestamp):
        if timestamp < time.time():
            raise BackendError("stop time already elapsed")
        if self._waiting_for_stop_time:
            self._stopID.cancel()
        self._waiting_for_stop_time = True
        self._stopID = reactor.callLater(
            timestamp - time.time(),
            self._stop_now
        )
