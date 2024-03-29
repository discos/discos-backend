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

import logging
import sys

from discosbackend import server
from discosbackend.handlers import DBProtocolHandler

from roach2_backend import Roach2_Backend  # pylint:disable=import-error

logging.basicConfig(filename='example.log', level=logging.DEBUG)

server.run_server(
    int(sys.argv[1]), DBProtocolHandler(Roach2_Backend())
)
