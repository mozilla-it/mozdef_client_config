#!/usr/bin/env python
"""
    Library class for a mozdef client, where the not-message-specific
    config comes from a file rather than from all arguments.
"""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2018 Mozilla Corporation

import os
import sys
#import mozdef_client
from mozdef_client import MozDefEvent
sys.dont_write_bytecode = True

try:
    # 2.7's module:
    from ConfigParser import NoOptionError
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    # 3's module:
    from configparser import ConfigParser, \
        NoOptionError


class ConfigFetchMixin(object):  # pylint: disable=too-few-public-methods
    """
        This is a mixin to grab the mozdef url from a config file which
        is dedicated to mozdef, instead of mozdef particulars being
        buried in config files for random other code

        The name of the class must end in 'MixIn' (any case) to pass pylint
    """

    CONFIG_FILE_LOCATIONS = ['mozdef_client_config.conf',
                             '/usr/local/etc/mozdef_client_config.conf',
                             '/etc/mozdef_client_config.conf']

    def _ingest_config_from_file(self, conf_file=None):
        """
            pull in config variables from a system file
        """
        if conf_file is None:
            conf_file = self.__class__.CONFIG_FILE_LOCATIONS
        if isinstance(conf_file, basestring):
            conf_file = [conf_file]
        config = ConfigParser()
        for filename in conf_file:
            if os.path.isfile(filename):
                try:
                    config.read(filename)
                    break
                except:  # pylint: disable=bare-except
                    # This bare-except is due to 2.7
                    # limitations in configparser.
                    pass
        return config


class ConfigedMozDefEvent(ConfigFetchMixin, MozDefEvent):
    """
        This is the wrapper class for MozDefEvent.
        * get the mozdef URL from a config file
        * optionally allow real-time event disabling
    """
    def __init__(self):
        """
            Create the ConfigedMozDefEvent object, which is a barely-wrapped
            MozDefEvent, where we get the mozdef URL from a config file.
        """
        _configfile = self._ingest_config_from_file()
        # We must have a URL in the config
        if not _configfile.has_section('mozdef'):
            raise ValueError('config file lacks a "mozdef" section')
        if not _configfile.has_option('mozdef', 'mozdef_url'):
            raise ValueError('config file lacks a "mozdef_url" option')
        url = _configfile.get('mozdef', 'mozdef_url')
        super(ConfigedMozDefEvent, self).__init__(url)

        # Turn the SSL verification on; we want this, and it gets noisy
        # when it's off.
        self.set_verify(True)

        # Try to pick up a boolean of whether to USE mozdef or not.
        # Default to 'yes, send events'
        try:
            _send_events = _configfile.getboolean('mozdef', 'send_events')
        except NoOptionError:
            _send_events = True
        self._send_events = _send_events

    def send(self, *args, **kwargs):
        """ A cutoff to avoid sending events """
        if self._send_events:
            super(ConfigedMozDefEvent, self).send(*args, **kwargs)


# Classes from upstream:
# class MozDefError         (no methods)
# class MozDefMessage       (not a leaf class)
# class MozDefMsg           (deprecated)
# class MozDefVulnerability (VPN does not report vulns)
# class MozDefEvent         (done)
# class MozDefRRA           (extension of MozDefEvent)
# class MozDefAssetHint     (extension of MozDefEvent)
# class MozDefCompliance    (extension of MozDefEvent)
