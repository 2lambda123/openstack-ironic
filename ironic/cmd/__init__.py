# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# NOTE(yuriyz): Do eventlet monkey patching here, instead of in
# ironic/__init__.py.  This allows the API service to run without monkey
# patching under Apache (which uses its own concurrency model). Mixing
# concurrency models can cause undefined behavior and potentially API timeouts.
import os

os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

import eventlet

eventlet.monkey_patch()
# Monkey patch the original current_thread to use the up-to-date _active
# global variable. See https://bugs.launchpad.net/bugs/1863021 and
# https://github.com/eventlet/eventlet/issues/592
# all the noqa below are for I202 due to 'import eventlet' above
import __original_module_threading as orig_threading  # noqa
import threading  # noqa
orig_threading.current_thread.__globals__['_active'] = threading._active

from ironic.common import i18n  # noqa

i18n.install('ironic')
