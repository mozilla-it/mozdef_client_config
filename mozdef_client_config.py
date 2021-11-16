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
    import configparser
except ImportError:  # pragma: no cover
    from six.moves import configparser

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

    def _ingest_config_from_file(self):
        """
            pull in config variables from a system file
        """
        conf_file = self.__class__.CONFIG_FILE_LOCATIONS
        config = configparser.ConfigParser()
        for filename in conf_file:
            if os.path.isfile(filename):
                try:
                    config.read(filename)
                    break
                except (configparser.Error):
                    pass
        return config


class ConfigedMozDefEvent(ConfigFetchMixin, MozDefEvent):  # pylint: disable=too-few-public-methods
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

        # Try to pick up a boolean of whether to USE mozdef or not.
        # Default to 'yes, send events'
        try:
            self._send_events = _configfile.getboolean('mozdef', 'send_events')
        except (configparser.NoOptionError, configparser.NoSectionError):
            self._send_events = True

        try:
            url = _configfile.get('mozdef', 'mozdef_url')
        except (configparser.NoOptionError, configparser.NoSectionError):
            if self._send_events:
                raise ValueError('config file lacks a "mozdef_url" option')
            url = 'undefined.hostname.company.local'

        super(ConfigedMozDefEvent, self).__init__(url)

        # Somewhat counterintuitively, we layer these settings on AFTER the super() call
        # because we want to assert our choices over top of the defaults that mozdef_client
        # sets on its own, that we can't actually control in the init process.

        # Turn on syslog logging via config
        try:
            self._send_to_syslog = _configfile.getboolean('mozdef', 'send_to_syslog')
        except (configparser.NoOptionError, configparser.NoSectionError):
            self._send_to_syslog = False

        # Allow to only send to syslog via config
        try:
            self._syslog_only = _configfile.getboolean('mozdef', 'syslog_only')
        except (configparser.NoOptionError, configparser.NoSectionError):
            self._syslog_only = False

        # Turn the SSL verification on; we want this, and it gets noisy
        # when it's off.
        self.set_verify(True)

    def send(self, *args, **kwargs):
        """ A cutoff to avoid sending events """
        if self._send_events:
            super(ConfigedMozDefEvent, self).send(*args, **kwargs)

    # wrap some properties that mozdef_client has used as internal
    # but that do not have exposed wrappers for otherwise.
    @property
    def category(self):
        """ GET the private _category variable in MozDefEvent """
        return self._category

    @category.setter
    def category(self, setval):
        """ SET the private _category variable in MozDefEvent """
        # As of 2018 the spec asks for lower-case categories
        self._category = setval.lower()  # pylint: disable=attribute-defined-outside-init

    @property
    def source(self):
        """ GET the private _source variable in MozDefEvent """
        return self._source

    @source.setter
    def source(self, setval):
        """ SET the private _source variable in MozDefEvent """
        self._source = setval  # pylint: disable=attribute-defined-outside-init

    # Properties not wrapped as there is presently not a need:
    # tags summary details
    # Methods used by passthrough:
    # set_severity_from_string syslog_convert

# Classes from upstream:
# class MozDefError         (no methods)
# class MozDefMessage       (not a leaf class)
# class MozDefMsg           (deprecated)
# class MozDefVulnerability (VPN does not report vulns)
# class MozDefEvent         (done)
# class MozDefRRA           (extension of MozDefEvent)
# class MozDefAssetHint     (extension of MozDefEvent)
# class MozDefCompliance    (extension of MozDefEvent)
